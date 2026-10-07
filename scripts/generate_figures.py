"""Generate deterministic PNG and PDF figures from verified event output."""
import argparse
import csv
import json
import hashlib
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def generate(results, output):
    summary=json.loads((results/"summary.json").read_text())
    audit=json.loads((results/"independent-check.json").read_text())
    digest=hashlib.sha256((results/"events.csv").read_bytes()).hexdigest()
    if digest != summary["events_sha256"] or digest != audit["events_sha256"] or audit["status"] != "PASS":
        raise ValueError("Derived table must match checked analysis and audit")
    if summary["validation"] != "PASS":
        raise ValueError("Analysis validation must pass first")
    with (results/"events.csv").open(newline="") as f:
        rows=list(csv.DictReader(f))
    if len(rows) != summary["events"]:
        raise ValueError("Event count mismatch")
    mass=summary["parent_mass_gev"]
    mt=np.array([float(r["transverse_mass_gev"]) for r in rows])
    disc=np.array([float(r["discriminant_gev4"]) for r in rows])
    output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,"savefig.dpi":180})
    def save(fig,name):
        fig.savefig(output/(name+".png"))
        fig.savefig(output/(name+".pdf"),metadata={"CreationDate":None,"ModDate":None,"Creator":"generate_figures.py"})
        plt.close(fig)
    fig,ax=plt.subplots(figsize=(7.2,4.5),layout="constrained")
    ax.hist(mt,bins=np.arange(0,802,2),histtype="step",color="#235789",linewidth=1.3)
    ax.axvline(mass,color="#b23a48",ls="--",label=f"Constraint mass {mass:g} GeV")
    ax.set(xlabel=r"$m_T$ [GeV]",ylabel="Events / 2 GeV",yscale="log",xlim=(0,800),title="CMS Open Data 5205: transverse mass")
    ax.text(.98,.93,f"100,000 events; overflow >= 800 GeV: {int(np.sum(mt>=800))}",transform=ax.transAxes,ha="right",fontsize=8)
    ax.legend(loc="upper right",bbox_to_anchor=(1,.86)); save(fig,"transverse-mass")
    fig,ax=plt.subplots(figsize=(7.2,4.5),layout="constrained")
    ax.scatter(mt-mass,disc,s=1,alpha=.2,rasterized=True,color="#235789")
    ax.axhline(0,color="black",lw=.7); ax.axvline(0,color="#b23a48",ls="--")
    ax.set(xlabel=r"$m_T-M_c$ [GeV]",ylabel=r"$D$ [GeV$^4$]",yscale="symlog",title=f"Fixed mass {mass:g} GeV: all 100,000 events")
    ax.set_yscale("symlog", linthresh=1e4)
    ax.set_yticks([-1e12,-1e10,-1e8,-1e6,-1e4,0,1e4,1e6,1e8,1e10])
    save(fig,"discriminant-boundary")

if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--results",type=Path,default=Path("scratch/primary"))
    p.add_argument("--output",type=Path,default=Path("figures"))
    a=p.parse_args(); generate(a.results,a.output)
