from random import randrange
from console import prompt, confirm


class Environment:
    generation = 0
    found_solution = False

    def __init__(self, individual, goal, population_size, crossover_rate, mutation_rate):
        self.individual = individual
        self.goal = goal
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

        self.population = self._generate_population()
        for i, individual in enumerate(self.population, 1):
            print('{:>5} --> {:>50} --> {:>10g} --> {:>10g}'.format(i, *individual.evaluate(self.goal)))

    def _generate_population(self):
        """Bangkitkan populasi acak dari individu"""
        return [self.individual() for _ in range(self.population_size)]

    def step(self):
        while not self.found_solution:
            print('\nGenerasi ke', self.generation)

            if confirm('Lanjut? [Y/n] '):
                self.generation += 1
            else:
                print('eksekusi berakhir')
                break

    def run(self, max_generation):
        while self.generation <= max_generation and not self.found_solution:
            print('\nGenerasi ke', self.generation)

            if not self.found_solution:
                self.generation += 1
            else:
                print('solusi ditemukan')
                break
        print('eksekusi berakhir')


class Individual:
    score = 0

    def __init__(self, gene_count, gene_size=1, blueprint=None):
        self.gene_count = gene_count
        self.gene_size = gene_size
        self.chromosome_len = gene_count * gene_size
        self.blueprint = blueprint

        self.chromosome = self._generate_chromosome()

    def _generate_chromosome(self):
        return [randrange(2) for _ in range(self.chromosome_len)]

    def crossover(self):
        pass

    def mutate(self):
        pass


class Numeral(Individual):

    def __init__(self):
        super().__init__(75, 4, {
            '0000': '0',
            '0001': '1',
            '0010': '2',
            '0011': '3',
            '0100': '4',
            '0101': '5',
            '0110': '6',
            '0111': '7',
            '1000': '8',
            '1001': '9',
            '1010': '+',
            '1011': '-',
            '1100': '*',
            '1101': '/'
        })

    def translate(self):
        size = self.gene_size
        need_num = True
        protein = ''
        chromosome_str = ''.join(map(str, self.chromosome))

        for i in range(0, self.chromosome_len, size):
            gene = chromosome_str[i:i+size]

            if gene == '1110' or gene == '1111':
                pass
            elif gene == '1010' or gene == '1011' or gene == '1100' or gene == '1101':
                if not need_num:
                    protein += self.blueprint[gene]
                    need_num = True
            else:
                if need_num:
                    protein += self.blueprint[gene]
                    need_num = False

        protein_len = len(protein)
        if protein_len % 2 == 0:
            protein = protein[:-1]

        output = None
        if protein_len == 0:
            output = 0
        elif protein_len == 1:
            output = int(protein)
        else:
            try:
                output = eval(protein)
            except ZeroDivisionError:
                output = 0

        return protein, output

    def evaluate(self, goal):
        protein, output = self.translate()

        fitness = None
        try:
            fitness = 1 / (goal - output)
        except ZeroDivisionError:
            fitness = 0

        return protein, output, fitness

    def mutate(self):
        super().mutate()

    def crossover(self):
        super().crossover()


def main():
    goal = prompt('Angka tujuan? [100] ', 100)
    population_size = prompt('Jumlah populasi per generasi? (x > 1) [10] ', 10, lambda x: x > 1)
    mutation_rate = prompt('Tingkat mutasi? (0 < x < 1) [0.01] ', 0.01, lambda x: 0 < x < 1)
    crossover_rate = prompt('Tingkat persilangan? (0 < x < 1) [0.90] ', 0.90, lambda x: 0 < x < 1)

    env = Environment(Numeral, goal, population_size, crossover_rate, mutation_rate)

    if confirm('Jalankan per generasi? [Y/n] '):
        env.step()
    else:
        max_generation = prompt('Generasi maksimal? [100] ', 100, lambda x: x > 1)
        env.run(max_generation)


if __name__ == '__main__':
    main()
