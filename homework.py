from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    phrase_abt_training_type: str = 'Тип тренировки'
    phrase_abt_duration: str = 'Длительность'
    phrase_abt_distance: str = 'Дистанция'
    phrase_abt_mean_speed: str = 'Ср. скорость'
    phrase_abt_calories: str = 'Потрачено ккал'

    def get_message(self) -> str:
        """Получение информационного сообщения о тренировке."""
        return (f'{self.phrase_abt_training_type}: {self.training_type}; '
                f'{self.phrase_abt_duration}: {self.duration:0.3f} ч.; '
                f'{self.phrase_abt_distance}: {self.distance:0.3f} км; '
                f'{self.phrase_abt_mean_speed}: {self.speed:0.3f} км/ч; '
                f'{self.phrase_abt_calories}: {self.calories:0.3f}.')


class Training:
    """Базовый класс тренировки."""

    MINUTES_IN_HOUR: int = 60
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Определите run в '
                                  f'{self.__class__.__name__}!')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration
                * self.MINUTES_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    AVERAGE_SPEED_IN_M: float = 0.278
    CALORIES_MULTIPLIER_1: float = 0.035
    CALORIES_MULTIPLIER_2: float = 0.029
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MULTIPLIER_1
                 * self.weight
                 + ((self.get_mean_speed() * self.AVERAGE_SPEED_IN_M) ** 2
                    / (self.height / self.CM_IN_M))
                 * self.CALORIES_MULTIPLIER_2
                 * self.weight)
                * self.duration * self.MINUTES_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MULTIPLIER: int = 2
    CALORIES_SHIFT: float = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_SHIFT)
                * self.CALORIES_MULTIPLIER
                * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_training = {'SWM': Swimming,
                         'RUN': Running,
                         'WLK': SportsWalking
                         }
    if workout_type in types_of_training:
        return types_of_training[workout_type](*data)
    raise TypeError(f'Ожидались следующие типы тренировки: SWM, RUN or WLK. '
                    f'Получено: "{workout_type}"')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
