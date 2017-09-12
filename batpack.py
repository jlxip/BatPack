#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import zipfile, random, os, base64


charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
def rzname(n=8):
	return ''.join(random.choice(charset) for _ in range(n))


def gfp(path, nd='', f='', PS=False):	# Get full path
	sep = '\\'
	if PS:
		sep += '\\'	# Un slash extra para escapar el slash del directorio
		if path[0] == '%':
			path = '$env:' + path.split('%')[1]
	fp = path + sep

	if not nd == '':
		fp += nd + sep
	if not f == '':
		fp += f

	if PS: fp = fp.replace(' ', '` ')

	return fp


if __name__ == '__main__':
	print 'B A T P A C K\n'

	print 'Enter files. Leave in blank when finished.'
	files = []
	while True:
		f = raw_input('[+] ')
		if f == '':
			break
		else:
			if os.path.isfile(f):
				files.append(f)
			else:
				print 'The file \'%s\' does not exist.' % f
	if len(files) == 0:
		print 'You have to enter at least one file.'
		exit()

	print '\n'

	possible_paths = ['%TEMP%', '.', '%APPDATA%']
	print 'Path of decompression:'
	for idx, v in enumerate(possible_paths):
		print '%i: %s' % (idx, v)
	path = raw_input('[0] ')
	if path == '': path = 0;
	if 0 <= int(path) < len(possible_paths):
		path = possible_paths[int(path)]
	else:
		print 'Invalid option.'
		exit()
	print '\n'
	
	print 'New directory? Leave in blank if not used.'
	nd = raw_input('[?] ')
	print '\n'

	print 'Select the file to be executed:'
	for idx, v in enumerate(files):
		print '%i: %s' % (idx, v)
	e = raw_input('[0] ')
	if e == '': e = 0
	if 0 <= int(e) < len(files):
		e = files[int(e)]
	else:
		print 'Invalid option.'
		exit()
	print '\n'

	print 'Delete decompressed files when execution is finished? (y/n)'
	df = raw_input('[y] ').lower()
	if df == '': df = 'y'
	if not df == 'y' and not df == 'n':
		print 'Invalid option.'
		exit()
	print '\n'

	# TODO: MELT

	print 'Internal zip name. Leave in blank for an 8 bytes alphanumeric random string.'
	zname = raw_input('[?] ')
	if zname == '': zname = rzname()
	print '\n'

	# TODO: OBFUSCATE BAT



	print '\n'
	print 'Compressing files...'
	zip = zipfile.ZipFile('tmp.zip', 'w', zipfile.ZIP_DEFLATED)
	for i in files:
		zip.write(i)
	zip.close()

	print 'Encoding zip file in memory...'
	b64 = base64.b64encode(open('tmp.zip', 'rb').read())
	os.remove('tmp.zip')	

	print 'Generating bat file in memory...'
	batcontent = '@echo %s>%s\r\n' % (b64, zname+'.txt')
	batcontent += '@certutil -decode \"{0}.txt\" \"{0}.zip\"\r\n'.format(zname)
	batcontent += '@powershell expand-archive \"%s.zip\" \"%s\"\r\n' % (zname, gfp(path, nd, '', True))
	batcontent += '@del \"{0}.txt\" \"{0}.zip\"\r\n'.format(zname)
	batcontent += '@\"%s\"\r\n' % gfp(path, nd, e)
	if df == 'y':
		batcontent += '@del '
		for f in files:
			batcontent += '\"'
			batcontent += gfp(path, nd, f)
			batcontent += '\" '
		batcontent += '\r\n'
		# TODO: REMOVE DIRECTORY IF NECESSARY

	print 'Writing bat file...'
	bat = open('packed.bat', 'w')
	bat.write(batcontent)
	bat.close()

	print 'Finished!'