import numpy as np
import _tetting
import _tetAI


level_difficulty_mapping = {1: 36,
                            2: 30,
                            3: 24,
                            4: 19,
                            5: 14,
                            6: 10,
                            7: 9,
                            8: 8,
                            9: 7,
                            10: 6,
                            11: 5,
                            12: 3}

class Simulation:

    def __init__(self, gen_size: int, n_allowed_to_reproduce: int, single_reproductions: int, max_mutation: float,
                 mutation_chance: int):
        self.gen_size = gen_size
        self.single_reproduction = single_reproductions
        self.max_mutation = max_mutation
        self.mutation_chance = mutation_chance
        self.n_for_reproduction = n_allowed_to_reproduce

        self.generation = 0
        self.tettings = np.array(
            [
                _tetting.Tetting(parents=None,
                                 max_mutation=self.max_mutation,
                                 mutation_chance=self.mutation_chance)
                for _ in range(self.gen_size)
            ])

        self.active_tetting: _tetting.Tetting = self.tettings[0]

        self.decision = []
        self.decision_index = 0
        self.tetting_index = 0
        self.dead_tetting_flag = False

    # Useless method?
    def run_generation(self):
        # TODO: Run all the tettings' games simultaneously
        for tetting in self.tettings:
            self.active_tetting: _tetting.Tetting = tetting
            while self.active_tetting.board.alive:
                self.active_tetting.act()

    def next_tetting(self):
        self.decision_index = 0
        if self.tetting_index == self.gen_size - 1:
            self.new_generation()
        else:
            self.tetting_index += 1
            self.active_tetting = self.tettings[self.tetting_index]

    def next_piece(self):
        self.active_tetting.decide()
        self.decision = self.active_tetting.decision
        self.active_tetting.next_piece_flag = False
        self.decision_index = 0

    def update(self):
        self.active_tetting.act(self.decision[self.decision_index])
        self.decision_index += 1
        self.dead_tetting_flag = False

        if self.active_tetting.board.level < 13:
            limiter = level_difficulty_mapping.get(self.active_tetting.board.level)
        else:
            limiter = 1

        if self.decision_index == limiter:
            self.active_tetting.board.pass_time()

        if self.active_tetting.next_piece_flag:
            self.next_piece()
        elif not self.active_tetting.board.alive:
            self.dead_tetting_flag = True
            self.next_tetting()

    def new_generation(self):
        tettings_fitness = [tetting.board.score for tetting in self.tettings]
        argsorted_tettings_fitness = np.argsort(tettings_fitness)[::-1]
        sorted_tettings_by_fitness: list[_tetting.Tetting] = [tetting for tetting in self.tettings[argsorted_tettings_fitness]]

        print(f"Best score in generation {self.generation}: ", sorted_tettings_by_fitness[0].board.score)

        self.generation += 1

        index = 0
        for top_tetting in sorted_tettings_by_fitness:
            if index == self.single_reproduction:
                break

            self.tettings[index] = _tetting.Tetting(parents=[top_tetting.brain],
                                                    max_mutation=self.max_mutation,
                                                    mutation_chance=self.mutation_chance)
            index += 1

        n_top_tettings_taken = int(self.n_for_reproduction / 2)

        #  Taking the best tetting for reproduction
        tettings_for_breeding = sorted_tettings_by_fitness[:n_top_tettings_taken]

        #  Taking some random Tettings
        for _ in range(int(np.ceil(self.n_for_reproduction / 2))):
            tettings_for_breeding.append(sorted_tettings_by_fitness[np.random.randint(n_top_tettings_taken + 1, self.gen_size)])

        #  The birds and the bees
        not_full = True
        while not_full:
            for first_tetting_index in range(self.n_for_reproduction):
                for second_tetting_index in range(first_tetting_index, self.n_for_reproduction):
                    self.tettings[index] = _tetting.Tetting(parents=[tettings_for_breeding[first_tetting_index].brain, tettings_for_breeding[second_tetting_index].brain],
                                                            max_mutation=self.max_mutation,
                                                            mutation_chance=self.mutation_chance)
                    index += 1
                    if index == self.gen_size:
                        break
                if index == self.gen_size:
                    break
            if index == self.gen_size:
                not_full = not not_full

        self.tetting_index = 0
