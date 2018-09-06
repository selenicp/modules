include modules/Makefile.inc

LOGDIR ?= log/exon_counts.$(NOW)
PHONY += dexseq

dexseq : $(foreach sample,$(TUMOR_SAMPLES),dex_seq/$(sample).taskcomplete)

define exon-count
dexseq/%.txt : star/bam/%.star.sorted.filtered.bam
	$$(call RUN,-c -s 8G -m 12G,"source /home/${USER}/share/usr/anaconda-envs/jrflab-modules.0.1.5/bin/activate /home/${USER}/share/usr/anaconda-envs/dexseq && \
								 /home/${USER}/share/usr/anaconda-envs/dexseq/lib/R/library/DEXSeq/python_scripts/dexseq_count.py -f bam /home/${USER}/share/reference/Ensembl/Homo_sapiens.GRCh37.75.gff $$< dexseq/$$*.txt")
dexseq/%.taskcomplete : dexseq/%.txt
	$$(call RUN,-c -s 1G -m 1G,"touch $$<")
endef
$(foreach sample,$(TUMOR_SAMPLES),\
		$(eval $(call exon-count,$sample)))

.DELETE_ON_ERROR:
.SECONDARY:
.PHONY: $(PHONY)