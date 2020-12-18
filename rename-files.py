from pathlib import Path 

path = Path('C:/Users/JWcam/Desktop/python-notes')

for p in path.iterdir():
	if p.is_file():
		extension = p.suffix
		old_name = str(p.stem)
		new_name = '-'.join(old_name.split())
		directory = p.parent
		p.replace(Path(directory, new_name + extension))
		print(Path(directory, new_name + extension))
