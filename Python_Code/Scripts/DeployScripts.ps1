
Write-Host "---------------------------------------------------------------"
Write-Host "Script to deploy all the Python files to process data"
Write-Host "---------------------------------------------------------------"

$env:PATHEXT += ";.py"

# Write-Host "Create the delay list"
# python .\Create_delay_list.py

Write-Host "Find the gap"
python .\find_gap.py

Write-Host "---------------------------------------------------------------"

Write-Host "Find the delay of hardware"
python .\get_gap_hw.py

Write-Host "---------------------------------------------------------------"

Write-Host "Difference btw delay"
python .\get_difference_between_delay.py

Write-Host "---------------------------------------------------------------"

# Best way is running in jupyter notebooks

# Write-Host "Jupyter notebook that calculate the sharp ratio"
# python .\Delay_Processing.py

# To create the sharp ratio for the individual users
# Write-Host "Jupyter notebook that calculate the sharp ratio"
# python .\ HEATMAP + KDE 


Write-Host "Apply the delay of hardware to the data"
python .\process_data_apply_dl_hw.py

Write-Host "---------------------------------------------------------------"

Write-Host "Move all txt and song files to a dir, that would be listed in Pure Data"
python .\Move_txt_and_wav.py
