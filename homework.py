class InfoMessage:
    """Ingormation message about training."""
    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f'Type training: {self.training_type}; '
            f'Duration: {self.duration:.3f} ч.; '
            f'Distance: {self.distance:.3f} км; '
            f'Midle speed: {self.speed:.3f} км/ч; '
            f'Spent calories: {self.calories:.3f}.')


class Training:
    """Base class training."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get distance in km/h."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get midle distance a move."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get quantity spent calories."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Return information message about complete training."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Traning run."""
    CALORIES_MEAN_SPEED_SHIFT: float = 20
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 - self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Training sport walk."""
    CALORIES_MEAN_SPEED_SHIFT: float = 0.035
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(
            action,
            duration,
            weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_SHIFT * self.weight + (
                self.get_mean_speed() ** 2 // self.height)
            * self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight)
            * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Training swimming."""
    LEN_STEP = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int
    ) -> None:
        super().__init__(
            action,
            duration,
            weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + 1.1) * 2 * self.weight)


def read_package(workout_type, data) -> Training:
    """Reads data give from sensors."""
    training_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Global function."""
    info = training.show_training_info()
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
