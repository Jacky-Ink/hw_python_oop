class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,  # затраченное время в часах
                 distance: float,  # расстояние в километрах
                 speed: float,  # скорость в км/ч
                 calories: float  # количество калорий
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # расстояние за один шаг
    M_IN_KM = 1000.0  # количество метров в километре

    def __init__(self,
                 action: int,  # количество совершенных действий
                 duration: float,  # затраченное время в часах
                 weight: float  # вес спортсмена
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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFFF_CALORIE_1 = 18
    COEFFF_CALORIE_2 = 20
    M_IN_HOUR = 60  # количество минут в часе

    def __init__(self,
                 action: int,  # количество совершенных действий
                 duration: float,  # затраченное время в часах
                 weight: float  # вес спортсмена
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.COEFFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFFF_CALORIE_2) * self.weight / self.M_IN_KM
                * self.duration * self.M_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFFF_CALORIE_3 = 0.035
    COEFFF_CALORIE_4 = 0.029
    COEFFF_CALORIE_5 = 2
    M_IN_HOUR = 60  # количество минут в часе

    def __init__(self,
                 action: int,  # количество совершенных действий
                 duration: float,  # затраченное время в часах
                 weight: float,  # вес спортсмена
                 height: float,  # рост спортсмена
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFFF_CALORIE_3 * self.weight + (self.get_mean_speed()
                ** self.COEFFF_CALORIE_5 // self.height)
                * self.COEFFF_CALORIE_4 * self.weight)
                * self.duration * self.M_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CCOEFF_CALORIE_5 = 2
    CCOEFF_CALORIE_6 = 1.1

    def __init__(self,
                 action: int,  # количество совершенных действий
                 duration: float,  # затраченное время в часах
                 weight: float,  # вес спортстмена
                 length_pool: float,  # длина бассейна
                 count_pool: int  # количество переплыбых бассейнов
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CCOEFF_CALORIE_6)
                * self.CCOEFF_CALORIE_5 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    reading = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    return reading[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
