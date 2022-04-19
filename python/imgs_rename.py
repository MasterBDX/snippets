import os
import pathlib
import itertools

path = pathlib.Path(__file__).parent.absolute()
counter = itertools.count()
for filename in os.listdir(path):
	old_path = path / filename
	name,ext = os.path.splitext(filename)
	new_path = path / ( str(next(counter)) + ext )
	# print(r'{}'.format(old_path))	
	if not filename.endswith('.py'):
		os.rename(r'{}'.format(old_path), r'{}'.format(new_path))