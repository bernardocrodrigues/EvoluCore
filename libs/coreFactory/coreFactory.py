
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
    def randomize_genes(cls,traits, genes):
        for gene in genes:

            gene_size = len(cls.genes_pool[gene])
            new_gene = cls.genes_pool[gene][np.random.randint(0, gene_size)]


            while new_gene == traits[gene]:
                new_gene = cls.genes_pool[gene][np.random.randint(0, gene_size)]

            traits[gene] = new_gene

        return traits



if __name__ == '__main__':

    a = ['8192', 'false', 'reg', '0', 'Sequential', 'true', 'no_div', '3', '1', '0', '13', 'Dynamic']

    print(factory.randomize_genes(a, [1,2,3]))