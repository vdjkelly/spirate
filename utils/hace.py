from datetime import datetime
from django.utils import timezone
from django.conf import settings

def hace(date_time):
	now = timezone.now()


	if isinstance(datetime, int):
		try:
			date_time = datetime.fromtimestamp(datetime)
		except ValueError:
			pass

	if isinstance(date_time, datetime):
		if settings.USE_TZ and timezone.is_naive(date_time):
			date_time = timezone.make_aware(date_time, timezone.get_current_timezone())
		diff = now - date_time

	else:
		return date_time

	seconds_diff = diff.seconds
	days_diff = diff.days

	if days_diff < 0:
		return ''

	if days_diff == 0:
		if seconds_diff < 10:
			return 'Hace unos instantes'
		if seconds_diff < 60:
			return 'Hace unos %s segundos' % seconds_diff
		if seconds_diff < 120:
			return 'Hace unos minutos'
		if seconds_diff < 3600:
			return 'Hace unos %s minutos' % (seconds_diff / 60)
		if seconds_diff < 7200:
			return 'Hace una hora'
		if seconds_diff < 86400:
			return 'Hace horas' % (seconds_diff / 3600)

	if days_diff == 1:
		return 'Ayer'
	if days_diff < 7:
		return 'Hace %s dias' % days_diff
	if days_diff < 14:
		return 'Hace una semana'
	if days_diff < 31:
		return 'Hace semanas ' % (days_diff / 7)
	if days_diff < 365:
		month_diff = days_diff / 30
		if month_diff == 1:
			return 'Hace un mes'
		else:
			return 'Hace meses %s' % (days_diff / 30)
	years_diff = days_diff / 365

	if years_diff == 1:
		return 'Hace un a&ntilde;o'
	return 'a&ntilde;o atras %s ' % (days_diff / 365)

