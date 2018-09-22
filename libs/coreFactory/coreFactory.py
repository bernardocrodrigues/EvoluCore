
import numpy as np

class factory(object):

    genes_pool = [['0', '1024', '2048', '4096', '8192'],
                  ['true', 'false'],
                  ['reg', 'ram'],
                  ['0', '1024', '2048', '4096', '8192'],
                  ['Sequential', 'None'],
                  ['true', 'false'],
                  ['no_div', 'srt2'],
                  ['0', '1', '2', '3'],
                  ['1', '0'],
                  ['1', '0'],
                  ['8', '12', '13'],
                  ['Dynamic', 'Static']]

    gene_names = ['dcache_size',
                  'dcache_bursts',
                  'dcache_victim_buf_impl',
                  'icache_size',
                  'icache_burstType',
                  'setting_support31bitdcachebypass',
                  'dividerType',
                  'mul_32_impl',
                  'shift_rot_impl',
                  'mul_64_impl',
                  'setting_bhtPtrSz',
                  'setting_branchpredictiontype']

    @classmethod
    def randomize_genes(cls, traits, genes):

        valid = False

        while not valid:
            for gene in genes:
                gene_size = len(cls.genes_pool[gene])
                new_gene = cls.genes_pool[gene][np.random.randint(0, gene_size)]
                while new_gene == traits[gene]:
                    new_gene = cls.genes_pool[gene][np.random.randint(0, gene_size)]
                aux = traits
                aux[gene] = new_gene
                if cls.validate_core(aux):
                    valid = True
                    traits = aux

        return traits

    @staticmethod
    def validate_core(traits):
        if traits[9] == '1' and (traits[7] == '1' or traits[7] == '0'):
            return False
        return True

    @classmethod
    def generate_random_cores(cls, num: int):

        cores = []

        while len(cores) < num:
            new_core = ()
            for gene in cls.genes_pool:
                new_core += (gene[np.random.randint(0, len(gene))],)
            if factory.validate_core(new_core) and not(new_core in cores):
                cores.append(new_core)

        return np.array(cores)

    @classmethod
    def format_core_dict(cls, core):

        aux = {}

        for gene, gene_name in zip(core, cls.gene_names):
            aux[gene_name] = gene

        return aux









if __name__ == '__main__':

    print(factory.generate_random_cores(10))
