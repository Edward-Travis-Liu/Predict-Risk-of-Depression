''' Select Target Variables '''
def get_lists():

	variables_list_1 = [
	'deprawsc',
	'degree_md',
	'degree_ass',
	'degree_bach',


	'age',
	'sex_birth',
	'race_black',
	'race_ainaan',
	'race_asian',
	'race_his',
	'race_pi',
	'race_mides',
	'race_white',
	'international',

	'fincur',
	'relship',
	'sexual_h',
	'sexual_l',
	'sexual_g',
	'sexual_bi',
	'sexual_queer',
	'sexual_quest',
	'sexual_asexual',
	'sexual_pan',
	'sexual_other',
	'religios',
	'height_ft',

	#selected by mutual information criterion ↓

	'anx_score',
	'dx_psy',
	'ed_scoff',
	'Eating_disorder',
	'abuse_life',
	'assault_emo',
	'sleep_wknight',
	'sa_exp',
	'exerc',
	'assault_phys',
	'sub_vape',
	'smok_freq',
	'Q3_22',
	'talk1_6',
	'drug_coc',
	]

	variables_list_2 = [
	'deprawsc','degree_md',
	'degree_ass',
	'degree_bach',

	'age','sex_birth','race_black','race_ainaan','race_asian','race_his','race_pi','race_mides','race_white','international',

	'fincur',
	'relship',
	'sexual_h','sexual_l','sexual_g','sexual_bi','sexual_queer','sexual_quest','sexual_other',
	'religios',
	'height_ft',

	'anx_score',
	'dx_psy',
	'ed_scoff',
	'Eating_disorder',
	'abuse_life',
	'assault_emo',
	'sleep_wk1',
	'sleep_wd1',
	'assault_sex',
	'exerc',
	'assault_phys',
	'smok_vape',
	'smok_freq',
	'risk_alc',
	'talk1_6',
	'drug_coc',
	]

	variables_list_3 = [
	'deprawsc','degree_md',
	'degree_ass',
	'degree_bach',

	'age','sex_birth','race_black','race_ainaan','race_asian','race_his','race_pi','race_mides','race_white','international',

	'fincur',
	'relship',
	'sexual_h','sexual_l','sexual_g','sexual_bi','sexual_queer','sexual_quest','sexual_other',
	'religios',
	'height_ft',

	'anx_score',
	'dx_psy',
	'ed_scoff',
	'binge',
	'abuse_life',
	'assault_emo',
	'sleep_wk1',
	'sleep_wd1',
	'assault_sex',
	'exerc',
	'assault_phys',
	#'smok_vape',
	'smok_freq',
	'risk_alc',
	'talk1_6',
	'drug_coc',
	]

	variables_list_4 = [
	'deprawsc','degree_md',
	'degree_ass',
	'degree_bach',

	'age','sex_birth','race_black','race_ainaan','race_asian','race_his','race_pi','race_mides','race_white','international',

	'fincur',
	'relship',
	'sexual_h','sexual_g',
	'religios',
	'height_ft',

	'anx_score',
	'dx_psy',
	'ed_scoff',
	'binge',
	'abuse_life',
	'assault_emo',
	'sleep_wk1',
	'sleep_wd1',
	'assault_sexr',
	#'exerc',
	'assault_phys',
	#'smok_vape',
	'smok_freq',
	'risk_alc',
	'talk1_6',
	'drug_coc',
	]

	variables_list_5 = [
	'deprawsc','deg_md','degree_full',

	'age','gender','race_bla',
	'race_ame',
	'race_asi',
	'race_his',
	'race_pac',
	'race_ara',
	'race_whi',
	'intnat',	

	'fincur',
	'relship',
	'sexual',
	'religios',
	'hgt_inch',

	'anx_score',
	'dx_psy',
	'ed_scoff',
	'dx_ea',
	#'abuse_life',
	#'assault_emo',
	'sleep_wk1',
	'sleep_wd1',
	#'assault_sexr',
	'exercise',
	#'voilence_vic',
	#'smok_vape',
	'smok_freq',
	#'dx_s',
	'inf_rel',
	'drug_coc',
	]

	return variables_list_1, variables_list_2, variables_list_3, variables_list_4, variables_list_5

''' Unified Names and Formats '''
def lables_unification(df, year):

		if year == 2017:
			df['smok_vape'] = -1
		elif year == 2016:
			df['exerc'] = -1
			df['smok_vape'] = -1
			df['risk_alc'] = -1
			df['sexual_l'] = 0
			df['sexual_bi'] = 0
			df['sexual_queer'] = 0
			df['sexual_quest'] = 0
			df['sexual_other'] = 0
		elif year == 2013:
			df['abuse_life'] = -1
			df['assault_emo'] = -1
			df['assault_sex'] = -1
			df['assault_phys'] = -1
			df['smok_vape'] = -1
			df['risk_alc'] = 0
			df['sexual_h'] = df['sexual'] + 1
			df['sexual_l'] = 0
			df['sexual_g'] = 2 - df['sexual']
			df['sexual_bi'] = 0
			df['sexual_queer'] = 0
			df['sexual_quest'] = 0
			df['sexual_other'] = 0
			df = df.drop(['sexual'], axis=1)

		if year != 2021:
			df['sleep_wknight'] = (df['sleep_wk1'] - df['sleep_wd1'] + 24) % 12
			df = df.drop(['sleep_wk1', 'sleep_wd1'], axis=1)
			df['sexual_asexual'] = 0
			df['sexual_pan'] = 0

		if year == 2013:
			df['graduate_student'] = df.apply(lambda row: 0 if row['degree_full'] == 1 or row['degree_full'] == 2 else 1, axis=1)
			df['race'] = df['race_bla']
			df['race'] = df['race'].combine_first(df['race_ame']*2).combine_first(df['race_asi']*3).combine_first(df['race_his']*4)
			df['race'] = df['race'].combine_first(df['race_pac']*5).combine_first(df['race_ara']*6).combine_first(df['race_whi']*7)
			df = df.drop(['degree_full','race_bla', 'race_ame', 'race_asi', 'race_his', 'race_pac', 'race_ara',	'race_whi'], axis=1)
		else:
			df['graduate_student'] = df.apply(lambda row: 0 if row['degree_ass'] == 1 or row['degree_bach'] == 1 else 1, axis=1)
			df['race'] = df['race_black']
			df['race'] = df['race'].combine_first(df['race_ainaan']*2).combine_first(df['race_asian']*3).combine_first(df['race_his']*4)
			df['race'] = df['race'].combine_first(df['race_pi']*5).combine_first(df['race_mides']*6).combine_first(df['race_white']*7)
			df = df.drop(['degree_ass','degree_bach','race_black', 'race_ainaan', 'race_asian', 'race_his', 'race_pi', 'race_mides', 'race_white'], axis=1)

		df['sexual'] = df['sexual_h']
		df['sexual'] = df['sexual'].combine_first(df['sexual_l']*2).combine_first(df['sexual_g']*3).combine_first(df['sexual_bi']*4)
		df['sexual'] = df['sexual'].combine_first(df['sexual_queer']*5).combine_first(df['sexual_quest']*6).combine_first(df['sexual_asexual']*7)
		df['sexual'] = df['sexual'].combine_first(df['sexual_pan']*8).combine_first(df['sexual_other']*9)
		df = df.drop(['sexual_h', 'sexual_l', 'sexual_g', 'sexual_bi', 'sexual_queer', 'sexual_quest', 'sexual_asexual', 'sexual_pan', 'sexual_other'], axis=1)

		#print(df.columns)
		df.rename(columns={
		'deprawsc': 'Depression_point',
		'degree_md': 'degree',
		'deg_md': 'degree',
		'sex_birth': 'gender',
		'intnat': 'international_student',
		'hgt_inch': 'height',
		'Q3_22': 'alcohol_abuse',
		'risk_alc': 'alcohol_abuse',
		'assault_sexr': 'assault_sex',
		'talk1_6': 'religious_emotional_help',
		'smok_freq': 'smoking_frequency',
		'exerc': 'exercise',
		'sleep_wknight': 'weekday_sleep_time',
		'anx_score': 'anxiety_score',
		'height_ft': 'height',
		'binge': 'Eating_disorder',
		'fincur': 'financial_status',
		'sub_vape': 'smok_vape',
		'sa_exp': 'assault_sex',
		'ab_emo_charc': 'assault_emo',
		'inf_rel': 'religious_emotional_help',
		'international': 'international_student',
		'dx_ea': 'Eating_disorder',
 		'ed_scoff': 'weight_gain',
		}, inplace=True)
		#print(df.columns)

		return df