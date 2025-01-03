import random
import ROOT
import argparse

outcomes = []

#parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, help='Number of tries to run', default=100)
args = parser.parse_args()

n_tries = args.n

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

c = ROOT.TCanvas("c","c",800,800)
c.SetGrid()
c.SetTicks()
c.SetLeftMargin(0.15)

## histograms
h_win = ROOT.TH1F("h_win",";Number of tries;Wins",n_tries,0.5,n_tries+0.5)
h_win.SetMarkerStyle(20)
h_win.SetMarkerColor(ROOT.kRed)

h_lost = ROOT.TH1F("h_lost",";Number of tries;Wins",n_tries,0.5,n_tries+0.5)
h_lost.SetMarkerStyle(20)
h_lost.SetMarkerColor(ROOT.kBlue)

for n_try in range(1,n_tries+1):
    ## assign all doors with 0 (no car)
    n_doors = 3
    doors_values = [0 for _ in range(n_doors)]

    ## choose randomly one door to put the car (=1)
    rand_idx = random.randint(0, len(doors_values)-1)
    doors_values[rand_idx] = 1

    ## randomly choose a door
    door_chosen = random.randint(0, len(doors_values)-1)

    ## find an empty door to open
    empty_door = -1
    while True:
        rand_idx = random.randint(0, len(doors_values)-1)
        if rand_idx != door_chosen and doors_values[rand_idx] == 0:
            empty_door = rand_idx
            break

    ## find the door that is left (not chosen and not the empty one selected in previous step)
    door_left = -1
    for index in range(n_doors):
        if index != empty_door and index != door_chosen: door_left = index

    ## make the decision to keep or switch doors (we always switch)
    answer = "y"
    door_final_answer = -1
    if answer == "y":
        door_final_answer = door_left
    else:
        door_final_answer = door_chosen

    ## save outcome
    [outcomes.append(1) if doors_values[door_final_answer] == 1 else outcomes.append(0)]

    ## fill histograms
    n_wins = outcomes.count(1)
    h_win.SetBinContent(n_try,n_wins)

    n_lost = outcomes.count(0)
    h_lost.SetBinContent(n_try,n_lost)

## print final result
print(f"After {n_tries} tries you won {round(outcomes.count(1)*100/n_tries,1)}% of times by switching doors")

## make plot with outcomes
## find which histogram to plot first
if h_win.GetMaximum() > h_lost.GetMaximum():
    h_win.Draw("p")
    h_lost.Draw("same p") 
else:
    h_lost.Draw("p")
    h_win.Draw("same p")

leg = ROOT.TLegend(0.2,0.7,0.35,0.85)
leg.SetBorderSize(0)
leg.AddEntry(h_win,"Switching","p")
leg.AddEntry(h_lost,"Staying","p")
leg.Draw()

latex = ROOT.TLatex()
latex.SetTextSize(0.025)
latex.DrawLatexNDC(0.15,0.905,f"After {n_tries} tries you won {round(outcomes.count(1)*100/n_tries,1)}% of times by switching doors")

c.SaveAs("outcomes.pdf")