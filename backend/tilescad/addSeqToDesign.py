import scadnano as sc
import pandas as pd

if __name__ == '__main__':
    input_des_name = '/home/trogers/Dropbox/core_tiles_strand_seq_design/TileScad/k10_canvas_dim8'
    output_des_name = 'test' #input_des_name + '_seq'

    input_idt_name = '/home/trogers/core_tiles_seq_design/periodic_t16_k5_l16_2022_01_11_07_08_02/structure_files/Structurek10_2022-01-11-07:22:23.idt'

    des = sc.Design.from_scadnano_file(input_des_name + '.sc')

    seq_df = pd.read_csv(input_idt_name, comment='#', names=['Name', 'Sequence', 'Amt', 'Prep'], index_col='Name')

    seq_dict = seq_df['Sequence'].to_dict()
    #print(seq_dict)
    for strand in des.strands:
        des.assign_dna(strand, ''.join( seq_dict[strand.name].split() ), assign_complement=False, check_length=True)

    des.write_scadnano_file(filename=output_des_name )