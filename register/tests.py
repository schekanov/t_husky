from datetime import datetime, time

from django.test import TestCase

from register.models import Master, CarBrand, CarModel, Schedule


class FixtureTestCase(TestCase):
    """ Тест фикстур"""

    fixtures = ['initial_data']

    def test_models_data(self):
        """ Проверяем загруженные в модели данные"""
        master = Master.objects.get(pk=3)
        self.assertEqual(master.name, 'Петрович')
        car_brand_count = CarBrand.objects.all().count()
        self.assertEqual(car_brand_count, 7)
        car_models = CarModel.objects.filter(name__startswith="Mod").values_list('name', flat=True).order_by('pk')
        self.assertListEqual([x for x in car_models], ['Model S', 'Model X', 'Model 3'])
        schedule_ids = Schedule.objects.filter(weekday__gte=5, is_workday=True
                                               ).values_list('pk', flat=True).order_by('pk')
        self.assertNotEqual([x for x in schedule_ids], [5, 6])


class ScheduleTestCase(TestCase):
    """ Проверка модели Schedule"""

    fixtures = ['initial_data']

    def test_check_date(self):
        """Тест проверки даты"""

        valid_date = datetime(2019, 1, 23, 11, 0, 0)
        invalid_time = datetime(2019, 1, 23, 8, 0, 0)
        invalid_date = datetime(2019, 1, 27, 11, 0, 0)

        self.assertEqual(Schedule.check_date(valid_date), True)
        self.assertEqual(Schedule.check_date(invalid_time), False)
        self.assertEqual(Schedule.check_date(invalid_date), False)

    def test_get_day_schedule(self):
        """Тест расписания на день"""

        workday = datetime(2019, 1, 23, 11, 0, 0)
        not_workday = datetime(2019, 1, 27, 11, 0, 0)

        res_wd = (True, time(10, 0, 0), time(20, 0, 0))
        res_nwd = (False, None, None)

        self.assertTupleEqual(Schedule.get_day_schedule(workday), res_wd)
        self.assertTupleEqual(Schedule.get_day_schedule(not_workday), res_nwd)
