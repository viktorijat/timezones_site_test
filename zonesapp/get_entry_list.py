from datetime import datetime, timedelta


def get_all_entries_list(entries):

    if entries:
        all_list = []
        for obj in entries:
            obj_time = timedelta(hours=obj.gmt_offset_display.hour, minutes=obj.gmt_offset_display.minute)
            now = datetime.now()
            current_time = (now + obj_time).strftime('%Y-%m-%d %H:%M:%S %Z%z')

            line = {'entry_id': str(obj.id), 'entry_name': str(obj.entry_name), 'city_name': str(obj.city_name),
<<<<<<< HEAD
                    'user': str(obj.user), 'entry_offset': str(obj.gmt_offset_display.strftime('%H:%M')), 'current_time': current_time}
=======
                    'user': str(obj.user), 'entry_offset': obj.gmt_offset_display.strftime('%H:%M'), 'current_time': current_time}
>>>>>>> 167299c35b3df50037a61277ccea4cc5db38d3e8
            all_list.append(line)

        return all_list
    else:
        return False