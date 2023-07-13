cd "C:\\Users\\EddyF\\workspaces\\sloubi\\build_win" || exit
pyinstaller --onefile --windowed --icon "C:\\Users\\EddyF\\workspaces\\sloubi\\graphics\\icon.ico" --name "sloubi" --add-data "C:\\Users\\EddyF\\workspaces\\sloubi\\src\\ion.py;." --add-data "C:\\Users\\EddyF\\workspaces\\sloubi\\graphics\\icon.ico;." --add-data "C:\\Python311\\Lib\\site-packages\\kandinsky;\\kandinsky" "C:\\Users\\EddyF\\workspaces\\sloubi\\src\\main.py"
read -n1 -r -p "Press any key to continue..."
