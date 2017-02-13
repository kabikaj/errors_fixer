
DATA_DIR=../../data/files

INP_PARENT_DIR=$(DATA_DIR)/jsondump
INP_OCRED_DIR=$(INP_PARENT_DIR)/ocred_texts
INP_ALTAFSIR_DIR=$(INP_PARENT_DIR)/altafsir
INP_HADITH_DIR=$(INP_PARENT_DIR)/hadith_alislam

OUT_PARENT_DIR=$(DATA_DIR)/errorsfixed
OUT_OCRED_DIR=$(OUT_PARENT_DIR)/ocred_texts
OUT_ALTAFSIR_DIR=$(OUT_PARENT_DIR)/altafsir
OUT_HADITH_DIR=$(OUT_PARENT_DIR)/hadith_alislam

RM=/bin/rm -f
PYTHON=/usr/bin/env python
ERROR_FIXER=errorfixer.py

.PHONY : clean help all fixerrors_ocred fixerrors_altafsir fixerrors_hadith

all: clean fixerrors_ocred fixerrors_altafsir fixerrors_hadith

fixerrors_ocred:
	@echo "\n>> Fixing errors in ocred texts..."
	$(PYTHON) $(ERROR_FIXER) $(INP_OCRED_DIR) $(OUT_OCRED_DIR)

fixerrors_altafsir:
	@echo "\n>> Fixing errors in altafsir files..."
	$(PYTHON) $(ERROR_FIXER) $(INP_ALTAFSIR_DIR) $(OUT_ALTAFSIR_DIR)

fixerrors_hadith:
	@echo "\n>> Fixing errors in hadith.al-islam files..."
	$(PYTHON) $(ERROR_FIXER) $(INP_HADITH_DIR) $(OUT_HADITH_DIR)

clean:
	@echo "\n>> Removing output files..."
	$(RM) $(OUT_OCRED_DIR)/*.json
	$(RM) $(OUT_ALTAFSIR_DIR)/*.json
	$(RM) $(OUT_HADITH_DIR)/*.json

help:
	@echo "    all"
	@echo "        Clean resources and fix errors in all sources"
	@echo "    fixerrors_ocred"
	@echo "        fix errors and adjust offsets for ocred texts"
	@echo "    fixerrors_altafsir"
	@echo "        fix errors and adjust offsets for altafsir source files"
	@echo "    fixerrors_hadith"
	@echo "        fix errors and adjust offsets for hadith.al-islam source files"
	@echo "    clean"
	@echo "        remove files in output folders"
	@echo ""
	@echo "usage: make [help] [all] [fixerrors_ocred] [fixerrors_altafsir] [fixerrors_hadith] [clean]"
