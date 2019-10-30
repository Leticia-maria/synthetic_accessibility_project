from pathlib import Path
import re
from ast import literal_eval
from stk import (
    BuildingBlock,
    ConstructedMolecule,
    cage,
)


def load_population(pop_path):
    '''Loads the population of molecules from the EA.'''
    with open(pop_path, 'r') as f:
        pop = []
        subpop = []
        if 'fitness' in pop_path:
            recording = True
        else:
            recording = False

        gen = 1

        for line in f:
            # Initial population treated differently.
            if gen == 1:
                if 'Population log:' in line:
                    recording = True
                    print('New generation - recording.')
                elif 'ConstructedMolecule' in line and recording:
                    subpop.append(line)
                elif 'Starting generation' in line and recording:
                    recording = False
                    pop.append(subpop)
                    subpop = []
                    gen += 1
            elif gen != 1:
                if 'Selecting members' in line:
                    recording = True
                    print('New generation - recording.')
                elif 'ConstructedMolecule' in line and recording:
                    subpop.append(line)
                elif 'Starting' in line or 'Successful' in line and recording:
                    recording = False
                    pop.append(subpop)
                    subpop = []
                    gen += 1
        return pop


def parse_population(pop):
    # Import modules from stk.
    stk_pop = []
    for sp in pop:
        subpop = []
        for mem in sp:
            p_bb = re.compile('(Const[^\t]+)')
            stk_mem = eval(p_bb.search(mem)[0])
            stk_mem.fitness_vector = literal_eval(
                re.search('\t(\[([^\,]+\,)+[^\]]+\])', mem).group(1))
            stk_mem.fitness_value = literal_eval(
                re.search('\d+\.\d+(?=$)', mem).group(0))
            subpop.append(stk_mem)
        stk_pop.append(subpop)
    return stk_pop


def get_stk_pop(pop_path):
    pop_path = Path(pop_path)
    pop = load_population(str(pop_path))
    pop = parse_population(pop)
    return pop


if __name__ == '__main__':
    print(get_stk_pop('/rds/general/user/sb2518/home/WORK/main_projects/synthetic_accessibility_project/stages/stage3_ea_analysis/create_image/example_pop.log'))
