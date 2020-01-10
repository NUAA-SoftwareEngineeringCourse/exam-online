# from datetime import datetime
#
# d = datetime.now()
# print(d.year)
# print(datetime.year())

s = '["27","25","26","28"]'
import json
l = list(json.loads(s))

print(l)

l[l.index('28')] = '29'

print(l)



# @app.route('/teacher_replace_judge_flush/', methods=['GET', 'POST'])
# def teacher_replace_judge_flush():
#     all_ids = json.loads(request.args.get('all_ids'))
#     source_id = request.args.get('source_id')
#     target_id = request.args.get('target_id')
#     print('[replace judge flush]', source_id, target_id)
#
#     print(all_ids)
#     judge_list = all_ids['judge']
#     judge_list[judge_list.index(source_id)] = target_id
#     print(all_ids)
#
#     import teacher_helper, admin_helper
#     choice_list = teacher_helper.get_question_list_by_ids(all_ids['choice'], choice_question_table)
#     judge_list = teacher_helper.get_question_list_by_ids(all_ids['judge'], judge_question_table)
#     subjective_list = teacher_helper.get_question_list_by_ids(all_ids['subjective'], subjective_question_table)
#     title_list = admin_helper.admin_get_questions_type()
#     return render_template('teacherQuestion.html', choice_list=choice_list, judge_list=judge_list,
#                            subjective_list=subjective_list, title_list=title_list,
#                            keyword='', xuanze='', panduan='', jianda='',
#                            nanti1='', nanti2='', nanti3='')