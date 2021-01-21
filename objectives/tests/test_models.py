from django.test import TestCase

from objectives.models import Objective, Goal


class ObjectiveModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.objective = Objective.objects.create(
            metric_name='Porcentaje de ventas',
            description='El procentaje debe ser mayor a 7'
        )

    def test_objective_string_representation(self):
        """Objective as string should be its metric_name"""
        string_objective = str(self.objective)
        
        self.assertEqual(string_objective, self.objective.metric_name)
    
    def test_absolute_url(self):
        """Objective absolute url should be /objetivos/:id"""
        absolute_url = self.objective.get_absolute_url()

        self.assertEqual(absolute_url, "/objetivos/%s" % self.objective.id)


class GoalModelTest(TestCase):
    def test_goal_string_representation(self):
        objective = Objective.objects.create(
            metric_name='Objetivo',
            description='Superar las ventas'
        )

        goal_string = 'Minimo'
        goal = Goal.objects.create(
            objective=objective,
            description=goal_string,
            value=1,
            percentage=50
        )

        self.assertEqual(str(goal), goal_string)


class NearestGoalsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        objective = Objective.objects.create(
            metric_name='Porcentaje X',
            description='Este objetivo es muy importante'
        )

        Goal.objects.bulk_create([
            Goal(objective=objective,
                 description='Minimo', value=5, percentage=80),
            Goal(objective=objective,
                 description='Medio', value=6, percentage=90),
            Goal(objective=objective,
                 description='Maximo', value=7, percentage=100)
        ])

        cls.objective = objective

        objective_inverse = Objective.objects.create(
            metric_name='Porcentaje Y',
            description='Este objetivo es muy importante'
        )

        Goal.objects.bulk_create([
            Goal(objective=objective_inverse,
                 description='Maximo', value=7, percentage=80),
            Goal(objective=objective_inverse,
                 description='Medio', value=6, percentage=90),
            Goal(objective=objective_inverse,
                 description='Minimo', value=5, percentage=100)
        ])

        cls.objective_inverse = objective_inverse

    def test_get_nearest_goals(self):
        """Getting nearest goals for an increasing goals set should return a valid tuple"""

        goal_set = self.objective.goal_set.all()
        nearest_goals = self.objective._get_nearest_goals(5.5)

        self.assertIsInstance(nearest_goals, tuple)
        self.assertEqual(len(nearest_goals), 2)

        left_goal = nearest_goals[0]
        right_goal = nearest_goals[1]

        self.assertEqual(left_goal.id, goal_set[0].id)
        self.assertEqual(right_goal.id, goal_set[1].id)

    def test_get_nearest_goals_existing(self):
        """Getting nearest goals for an existing value should return the single Goal"""

        nearest_goals = self.objective._get_nearest_goals(5)

        self.assertIsInstance(nearest_goals, Goal)
        self.assertEqual(self.objective.goal_set.first().id, nearest_goals.id)

    def test_get_nearest_goals_inverse(self):
        """Getting nearest goals for an decreasing goals set should return a valid tuple"""

        goal_set = self.objective_inverse.goal_set.all()
        nearest_goals = self.objective_inverse._get_nearest_goals(5.5)

        self.assertIsInstance(nearest_goals, tuple)
        self.assertEqual(len(nearest_goals), 2)

        left_goal = nearest_goals[0]
        right_goal = nearest_goals[1]

        self.assertEqual(left_goal.id, goal_set[1].id)
        self.assertEqual(right_goal.id, goal_set[2].id)

    def test_get_nearest_goals_min(self):
        """Getting nearest goals for a value less than the increasing goals set should return a valid tuple"""

        goal_set = self.objective.goal_set.all()
        nearest_goals = self.objective._get_nearest_goals(4)

        self.assertIsInstance(nearest_goals, tuple)
        self.assertEqual(len(nearest_goals), 2)

        left_goal = nearest_goals[0]
        right_goal = nearest_goals[1]

        self.assertIs(left_goal, None)
        self.assertEqual(right_goal.id, goal_set[0].id)

    def test_get_nearest_goals_max(self):
        """Getting nearest goals for a value greater than the increasing goals set should return a valid tuple"""

        goal_set = self.objective.goal_set.all()
        nearest_goals = self.objective._get_nearest_goals(9)

        self.assertIsInstance(nearest_goals, tuple)
        self.assertEqual(len(nearest_goals), 2)

        left_goal = nearest_goals[0]
        right_goal = nearest_goals[1]

        self.assertEqual(left_goal.id, goal_set[2].id)
        self.assertIs(right_goal, None)

    def test_get_nearest_goals_inverse_min(self):
        """Getting nearest goals for a value less than a decreasing goals set should return a valid tuple"""

        goal_set = self.objective_inverse.goal_set.all()
        nearest_goals = self.objective_inverse._get_nearest_goals(4)

        self.assertIsInstance(nearest_goals, tuple)
        self.assertEqual(len(nearest_goals), 2)

        left_goal = nearest_goals[0]
        right_goal = nearest_goals[1]

        self.assertEqual(left_goal.id, goal_set[2].id)
        self.assertIs(right_goal, None)

    def test_get_nearest_goals_inverse_max(self):
        """Getting nearest goals for a value greater than a decreasing goals set should return a valid tuple"""

        goal_set = self.objective_inverse.goal_set.all()
        nearest_goals = self.objective_inverse._get_nearest_goals(9)

        self.assertIsInstance(nearest_goals, tuple)
        self.assertEqual(len(nearest_goals), 2)

        left_goal = nearest_goals[0]
        right_goal = nearest_goals[1]

        self.assertIs(left_goal, None)
        self.assertEqual(right_goal.id, goal_set[0].id)

    def test_calculate_percentage_existing(self):
        """Calculating percentage for existing value should return the corresponding value"""

        result = self.objective.calculate_percentage(5)
        self.assertEqual(result, 80)
    
    def test_calculate_percentage(self):
        """Calculating percentage for value between two goals should return its linear interpolation"""

        result = self.objective.calculate_percentage(5.5)
        self.assertEqual(result, 85)
    
    def test_calculate_percentage_min(self):
        """Calculating percentage for a value less than an increasing goals set should return 0"""

        result = self.objective.calculate_percentage(2)
        self.assertEqual(result, 0)

    def test_calculate_percentage_max(self):
        """Calculating percentage for a value greater than an increasing goals set should return 100"""

        result = self.objective.calculate_percentage(10)
        self.assertEqual(result, 100)
    
    def test_calculate_percentage_inverse_min(self):
        """Calculating percentage for a value less than an decreasing goals set should return 100"""

        result = self.objective_inverse.calculate_percentage(2)
        self.assertEqual(result, 100)

    def test_calculate_percentage_inverse_max(self):
        """Calculating percentage for a value greater than an decreasing goals set should return 0"""

        result = self.objective_inverse.calculate_percentage(10)
        self.assertEqual(result, 0)
