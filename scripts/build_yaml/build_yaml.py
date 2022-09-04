import os
from datetime import datetime
class Build_File(object):
	NECESSARY_FILE_NAME_DIC = {
		'custom_yaml_filename': 'cangjie3.custom.yaml', 
		'dict_template_filename': 'cangjie3.dict.template.yaml', 
		'schema_filename': 'cangjie3.schema.yaml', 
		'codechart_filename': 'cj3.txt', 
		'supplement_codechart_filename': 'cj3_supplement.txt', 
	}
	OUTPUT_FILE_NAME_DIC = {
		'custom_yaml_filename': 'cangjie3.custom.yaml', 
		'dict_yaml_filename': 'cangjie3.dict.yaml', 
		'schema_filename': 'cangjie3.schema.yaml', 
	}
	OUTPUT_TYPE_DIRNAME = {
		'kanji_only': '僅漢字', 
		'kanji_and_supplements': '包含部首筆畫兼容區漢字', 
	}
	MSCJ_PREPROCESSING_DIRNAME = {
		'before2004': 'Windows 10 2004之前的版本', 
		'after2004': 'Windows 10 2004及之后的Windows'
	}
	MSCJ_DIRNAME = "MSCJ予処理%s" % datetime.today().strftime('%Y%m%d_%H:%M:%S:%m')
	
	@classmethod
	def build_yaml(cls):
		source_file_path = os.path.realpath(__file__)
		source_file_path = '/'.join(source_file_path.split('/')[0:-1])
		source_file_path += '/source_file'
		#print(source_file_path)
		for file_name in Build_File.NECESSARY_FILE_NAME_DIC:
			necessary_file_path = "%s/%s" % (source_file_path, Build_File.NECESSARY_FILE_NAME_DIC[file_name])
			if not os.path.isfile(necessary_file_path):
				raise Exception("%s does not exists. " % necessary_file_path)
		os.chdir(source_file_path)
		#os.system('pwd')
		date_now = datetime.today().strftime('%Y%m%d')
		yaml_directory_abspath_name = '../RimeData_%s_Cangjie3_WithExtH' % date_now
		try:            #make directories
			os.mkdir(yaml_directory_abspath_name)
		except:
			pass
		for output_type in Build_File.OUTPUT_TYPE_DIRNAME:
			try:
				os.mkdir("%s/%s" % (yaml_directory_abspath_name, Build_File.OUTPUT_TYPE_DIRNAME[output_type]))
			except:
				pass
		os.mkdir('../%s' % Build_File.MSCJ_DIRNAME)
		for mscj_pre_dir in Build_File.MSCJ_PREPROCESSING_DIRNAME:
			os.mkdir('../%s/%s' % (Build_File.MSCJ_DIRNAME, Build_File.MSCJ_PREPROCESSING_DIRNAME[mscj_pre_dir]))

		for output_type in Build_File.OUTPUT_TYPE_DIRNAME:     #remove old files
			for output_file_name in Build_File.OUTPUT_FILE_NAME_DIC:
				try:
					os.remove("%s/%s/%s" % (yaml_directory_abspath_name, Build_File.OUTPUT_TYPE_DIRNAME[output_type], Build_File.OUTPUT_FILE_NAME_DIC[output_file_name]))
				except:
					pass
		for output_type in Build_File.OUTPUT_TYPE_DIRNAME:    #copy files
			os.system("cp '%s' '%s/%s/%s' " % (Build_File.NECESSARY_FILE_NAME_DIC['custom_yaml_filename'], yaml_directory_abspath_name, Build_File.OUTPUT_TYPE_DIRNAME[output_type], Build_File.OUTPUT_FILE_NAME_DIC['custom_yaml_filename']))
			os.system("cp '%s' '%s/%s/%s' " % (Build_File.NECESSARY_FILE_NAME_DIC['dict_template_filename'], yaml_directory_abspath_name, Build_File.OUTPUT_TYPE_DIRNAME[output_type], Build_File.OUTPUT_FILE_NAME_DIC['dict_yaml_filename']))
			os.system("cp '%s' '%s/%s/%s' " % (Build_File.NECESSARY_FILE_NAME_DIC['schema_filename'], yaml_directory_abspath_name, Build_File.OUTPUT_TYPE_DIRNAME[output_type], Build_File.OUTPUT_FILE_NAME_DIC['schema_filename']))
		
		os.system("cat %s | dos2unix | tail +9 | awk '{print $2 \"\t\" $1}' >> '%s/%s/%s'" % (Build_File.NECESSARY_FILE_NAME_DIC['codechart_filename'], yaml_directory_abspath_name, Build_File.OUTPUT_TYPE_DIRNAME['kanji_only'], Build_File.OUTPUT_FILE_NAME_DIC['dict_yaml_filename']))
		os.system("cat %s | dos2unix | awk '$3 == \"中日韓帶圈字符及月份\" {print $2 \"\t\" $1}' >> '%s/%s/%s'" % (Build_File.NECESSARY_FILE_NAME_DIC['supplement_codechart_filename'], yaml_directory_abspath_name, Build_File.OUTPUT_TYPE_DIRNAME['kanji_only'], Build_File.OUTPUT_FILE_NAME_DIC['dict_yaml_filename']))
		os.system("cat %s | dos2unix | awk '$3 == \"中日韓兼容字符\" {print $2 \"\t\" $1}' >> '%s/%s/%s'" % (Build_File.NECESSARY_FILE_NAME_DIC['supplement_codechart_filename'], yaml_directory_abspath_name, Build_File.OUTPUT_TYPE_DIRNAME['kanji_only'], Build_File.OUTPUT_FILE_NAME_DIC['dict_yaml_filename']))
		os.system("truncate -s -1 '%s/%s/%s'" % (yaml_directory_abspath_name, Build_File.OUTPUT_TYPE_DIRNAME['kanji_only'], Build_File.OUTPUT_FILE_NAME_DIC['dict_yaml_filename']))

		os.system("cat %s | dos2unix | tail +9 | awk '{print $2 \"\t\" $1}' >> '%s/%s/%s'" % (Build_File.NECESSARY_FILE_NAME_DIC['codechart_filename'], yaml_directory_abspath_name, Build_File.OUTPUT_TYPE_DIRNAME['kanji_and_supplements'], Build_File.OUTPUT_FILE_NAME_DIC['dict_yaml_filename']))
		os.system("cat %s | dos2unix | awk '{print $2 \"\t\" $1}' >> '%s/%s/%s'" % (Build_File.NECESSARY_FILE_NAME_DIC['supplement_codechart_filename'], yaml_directory_abspath_name, Build_File.OUTPUT_TYPE_DIRNAME['kanji_and_supplements'], Build_File.OUTPUT_FILE_NAME_DIC['dict_yaml_filename']))
		os.system("truncate -s -1 '%s/%s/%s'" % (yaml_directory_abspath_name, Build_File.OUTPUT_TYPE_DIRNAME['kanji_and_supplements'], Build_File.OUTPUT_FILE_NAME_DIC['dict_yaml_filename']))

		os.system("cat %s | dos2unix | tail +9 | awk '{print $1 \"\t\" $2}' > '%s/%s/%s'" % (Build_File.NECESSARY_FILE_NAME_DIC['codechart_filename'], '../', Build_File.MSCJ_DIRNAME, 'MSCJ_Pre.txt'))
		os.system("cat %s | dos2unix | awk '$3 == \"中日韓帶圈字符及月份\" {print $1 \"\t\" $2}' >> '%s/%s/%s'" % (Build_File.NECESSARY_FILE_NAME_DIC['supplement_codechart_filename'], '../', Build_File.MSCJ_DIRNAME, 'MSCJ_Pre.txt'))
		os.system("cat %s | dos2unix | awk '$3 == \"中日韓兼容字符\" {print $1 \"\t\" $2}' >> '%s/%s/%s'" % (Build_File.NECESSARY_FILE_NAME_DIC['supplement_codechart_filename'], '../', Build_File.MSCJ_DIRNAME, 'MSCJ_Pre.txt'))
		os.system("truncate -s -1 '%s/%s/%s'" % ('../', Build_File.MSCJ_DIRNAME, 'MSCJ_Pre.txt'))

		os.system('7z a %s.7z %s' % (yaml_directory_abspath_name, yaml_directory_abspath_name))


if __name__ == "__main__":
	Build_File.build_yaml()
