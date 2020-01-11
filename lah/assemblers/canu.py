import os

def keep_file_patterns():
    return [
        "*.seqStore/readNames.txt",
        "*.report",
        "*.unitigs.layout.readToTig",
        "*.unitigs.layout.tigInfo",
        "*.unitigs.fasta",
        "*.unitigs.gfa",
        "*.unitigs.bed",
        "*.contigs.layout.readToTig",
        "*.contigs.layout.tigInfo",
        "*.contigs.fasta",
        "*.contigs.gfa",
        "*.unassembled.fasta",
        "unitigging/4-unitigger/*.best.edges.gfa",
        "unitigging/4-unitigger/*.initial.assembly.gfa",
        "unitigging/4-unitigger/*.final.assembly.gfa",
        "unitigging/4-unitigger/*.contigs.gfa",
        "unitigging/4-unitigger/*.unitigs.gfa",
        "unitigging/4-unitigger/*.unitigs.bed",
        "unitigging/4-unitigger/*.contigs.aligned.gfa",
        "unitigging/4-unitigger/*.contigs.aligned.gfa.err",
        "unitigging/4-unitigger/*.unitigs.aligned.gfa",
        "unitigging/4-unitigger/*.unitigs.aligned.gfa.err",
        "unitigging/4-unitigger/*.unitigs.aligned.bed",
        "unitigging/4-unitigger/*.unitigs.aligned.bed.err",
        "unitigging/4-unitigger/*.contigs.aligned.bed",
        "unitigging/4-unitigger/*.contigs.aligned.bed.err",
    ]

#-- keep_file_patterns
