import numpy as np
last_n_games = 20
scoring = np.array([1,1,1,1,1,1,2,2,2,2,4,4,8])
num_games = len(scoring)
def score(strat, scenario):
    return (strat == scenario).dot(scoring)


class team:
    def __init__(self, name, rank, afc):
        self.name = name
        self.rank = rank
        self.afc = afc
    def __lt__(self, other):
        return self.rank < other.rank
    def __repr__(self):
        return self.name

class game:
    def __init__(self, t1, t2):
        self.t1=t1
        self.t2=t2
    def __iter__(self):
        if self.t1.rank < 7:
            yield self.t1
        if self.t2.rank < 7:
            yield self.t2
    def __repr__(self):
        return str(self.t1) + " vs " + str(self.t2)


class round:
    def __init__(self, games):
        self.games = games

    def __iter__(self):
        from copy import deepcopy
        possible_outcomes = [[]]
        for game in self.games:
            new_poss_outcomes = []
            for possible_winner in game:
                possible_outcomes_copy = deepcopy(possible_outcomes)
                for outcome in possible_outcomes_copy:
                    outcome.append(possible_winner)
                new_poss_outcomes.extend(possible_outcomes_copy)
            possible_outcomes = new_poss_outcomes
        for outcome in possible_outcomes:
            yield outcome

class tournament:
    def __init__(self, afc, nfc):
        self.afc = afc
        self.nfc = nfc

    def __iter__(self):
        import numpy as np
        ret = [""]*num_games
        r1_games = [game(self.afc[i], self.afc[7-i]) for i in range(1,4)]
        r1_games.extend(game(self.nfc[i], self.nfc[7-i]) for i in range(1,4))
        #afc_games_round_one = [game(self.afc[i], self.afc[7-i]) for i in range(1,4)]
        #ret[0:3] = afc_games_round_one
        #nfc_games_round_one = [game(self.nfc[i], self.nfc[7-i]) for i in range(1,4)]
        #ret[3:6] = nfc_games_round_one
        round1 = round(r1_games)
        for potential_round1_winners in round1:
            #print("potential_round1_winners = " + str(potential_round1_winners))
            ret[0:6] = [i.name for i in potential_round1_winners]
            round2 = round(games_from_round_1(potential_round1_winners, self.afc[0], self.nfc[0]))
            for potential_round2_winners in round2:
                ret[6:10] = [i.name for i in potential_round2_winners]
                round3 = round(games_from_round_2(potential_round2_winners))
                for potential_round3_winners in round3:
                    ret[10:12] = [i.name for i in potential_round3_winners]
                    round4 = round(games_from_round_3(potential_round3_winners))
                    for potential_round4_winner_in_list in round4:
                        ret[12] = potential_round4_winner_in_list[0].name
                        yield np.array(ret)

def games_from_round_1(winners, afc_one_seed, nfc_one_seed):
    afcs = [i for i in winners if i.afc]
    nfcs = [i for i in winners if not i.afc]
    afcs.append(afc_one_seed)
    nfcs.append(nfc_one_seed)
    afcs.sort()
    nfcs.sort()
    ret = [game(afcs[i], afcs[3-i]) for i in range(2)]
    ret.extend(game(nfcs[i], nfcs[3-i]) for i in range(2))
    return ret

def games_from_round_2(winners):
    afcs = [i for i in winners if i.afc]
    nfcs = [i for i in winners if not i.afc]
    return [game(afcs[0], afcs[1]),game(nfcs[0], nfcs[1])]

def games_from_round_3(winners):
    return [game(winners[0], winners[1])]
chiefs = "chiefs"
bills = "bills"
raiders = "raiders"
bucs = "bucs"
cowboys = "cowboys"
rams = "rams"
titans = "titans"
packers = "packers"
bengals = "bengals"
niners = "49ers"
cardinals = "cardinals"
patriots = "patriots"
steelers = "steelers"
eagles = "eagles"
afc = [
    team(titans, 1, True),
    team(chiefs, 2, True),
    team(bills, 3, True),
    team(bengals, 4, True),
    team(raiders, 5, True),
    team(patriots, 6, True),
    team(steelers, 7, True),
]

nfc = [
    team(packers, 1, False),
    team(bucs, 2, False),
    team(cowboys, 3, False),
    team(rams, 4, False),
    team(cardinals, 5, False),
    team(niners, 6, False),
    team(eagles, 7, False),
]

def find_best_strat(others_strats):
    best_prob_win = -1
    best_strat = None
    count = 0
    best_c = -1
    for strat in tournament(afc, nfc):
        count +=1
        #print("trying strat = "+str(strat))
        prob_win = calulate_win_prob(strat, others_strats)
        if prob_win > best_prob_win:
            best_prob_win = prob_win
            best_strat = strat
            best_c = count
            print("New best!")
        print("strat#: " + str(count) + "/2048\nstrat: " + str(strat) + "\nwin prob: " + str(prob_win) + "%\nbest win prob: " + str(best_prob_win) + "\n\n")
    print("best strat#: " + str(best_c) + "/2048\nstrat: " + str(best_strat) + "\nwin prob: " + str(best_prob_win) + "%\n\n")
    return best_strat

def calulate_win_prob(my_strat, others_strats):
    win_count = 0
    count = 0
    for scenario in tournament(afc, nfc):
        #print("against scenario = "+str(scenario))
        count += 1
        my_points = score(my_strat, scenario)
        their_points = [score(their_strat, scenario) for their_strat in others_strats]
        their_high = max(their_points)
        # if all((my_strat == scenario)[:10]):
        #     print(scenario)
        #print((my_strat == scenario))
        #print(all(my_strat == scenario))
        # if all(my_strat == scenario):
        #     print("YOO"*100)
        if their_high < my_points:
            win_count += 1
            continue
        #else:
            #print(their_high)
            #print(my_points)
            #print()
    return win_count / count




del_valle = np.array([chiefs, bills, raiders, bucs, cowboys, rams, titans, chiefs, packers, cowboys, titans, packers, titans])
caleb = np.array([chiefs, bills, bengals, bucs, niners, cardinals, bengals, chiefs, packers, bucs, chiefs, packers, packers])
z = np.array([chiefs, bills, bengals, bucs, cowboys, cardinals, titans, chiefs, packers, cowboys, chiefs, packers, chiefs])
ray = np.array([chiefs, bills, bengals, eagles, cowboys, cardinals, bengals, bills, packers, cowboys, bengals, cowboys, bengals])
mitch = np.array([chiefs, bills, bengals, bucs, cowboys, rams, bengals, bills, packers, bucs, bills, bucs, bucs])
kyle = np.array([chiefs, patriots, bengals, bucs, cowboys, cardinals, titans, chiefs, cardinals, bucs, titans, bucs, bucs])





best = find_best_strat([del_valle, caleb, z, ray, mitch, kyle])
print("best = " +str(best))
#print("strat#: " + str(2) + "/2048\nstrat: " + str(np.array([chiefs, bills, raiders, bucs, cowboys, rams, titans, chiefs, packers, cowboys, titans, packers, titans])) + "\nwin prob: " + str(1) + "%\nbest win prob: " + str(1) + "\n\n")
if __name__ == "__main__":
    pass

#print(calulate_win_prob(np.array([chiefs, bills, raiders, bucs, cowboys, rams, titans, chiefs, packers, cowboys, titans, packers, packers]), [np.array([chiefs, bills, raiders, bucs, cowboys, rams, titans, chiefs, packers, cowboys, titans, packers, titans])]))