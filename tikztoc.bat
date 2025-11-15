@echo off

echo Creating CMM TOC pdf files from source

setlocal

pushd tocs

REM /c for prod and /k for debug
set "CFLAG=/c"

start "CMM ALL" cmd /c "qt toc C:\Users\steve\S\TELOS\CMM_CAS\source cmm-all.tex -c 4 -m 1.5cm -w 7cm -o "{.unnumbered}" -o "About the Authors" && lualatex -interaction=batchmode cmm-all.tex && cmm-all.pdf"

start "CMM ONE" cmd /c "qt toc C:\Users\steve\S\TELOS\CMM_CAS\source cmm-1.tex -c 4 -m 1.5cm -w 7cm -o "{.unnumbered}" -o "About the Authors" -v 1 && lualatex -interaction=batchmode cmm-1.tex && cmm-1.pdf"

start "CMM TWO" cmd /c "qt toc C:\Users\steve\S\TELOS\CMM_CAS\source cmm-2.tex -c 4 -m 1.5cm -w 7cm -o "{.unnumbered}" -o "About the Authors" -v 2 && lualatex -interaction=batchmode cmm-2.tex && cmm-2.pdf"

start "CMM THREE" cmd /c "qt toc C:\Users\steve\S\TELOS\CMM_CAS\source cmm-3.tex -c 4 -m 1.5cm -w 7cm -o "{.unnumbered}" -o "About the Authors" -v 3 && lualatex -interaction=batchmode cmm-3.tex && cmm-3.pdf"

REM start "CMM CH4" cmd /c "qt toc C:\Users\steve\S\TELOS\CMM_CAS\source cmm-ch4.tex -c 4 -m 1.5cm -w 7cm -o "{.unnumbered}" -o "About the Authors" -p 4 && lualatex -interaction=batchmode cmm-ch4.tex && cmm-ch4.pdf"

popd
