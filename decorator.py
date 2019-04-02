from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []

        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,

            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):

    BASE_TESTIMONIAL = ("Strength", "Perception", "Endurance", "Charisma", "Intelligence", "Agility", "Luck")

    def __init__(self, base):
        self.base = base

    # Возвращает итоговые хараетеристики
    # после применения эффекта
    @abstractmethod
    def get_stats(self):
        pass

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass


class AbstractPositive(AbstractEffect):

    def get_stats(self):
        pass

    def get_positive_effects(self):
        positiveEffects = self.base.get_positive_effects()
        positiveEffects.append(self.__class__.__name__)
        return positiveEffects

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractNegative(AbstractEffect):

    def get_stats(self):
        pass

    def get_positive_effects(self):
        return self.base.get_positive_effects()

    def get_negative_effects(self):
        negativeEffects = self.base.get_negative_effects()
        negativeEffects.append(self.__class__.__name__)
        return negativeEffects


class Berserk(AbstractPositive):

    def get_stats(self):
        stats = self.base.get_stats()
        for k in stats.keys():
            if k in ("Strength", "Endurance", "Agility", "Luck"):
                stats[k] += 7
            if k in ("Perception", "Charisma", "Intelligence"):
                stats[k] -= 3
            if k == "HP":
                stats[k] += 50

        return stats


class Blessing(AbstractPositive):

    def get_stats(self):
        stats = self.base.get_stats()
        for k in stats.keys():
            if k in self.BASE_TESTIMONIAL:
                stats[k] += 2

        return stats


class Weakness(AbstractNegative):

    def get_stats(self):
        stats = self.base.get_stats()
        for k in stats.keys():
            if k in ("Strength", "Endurance", "Agility"):
                stats[k] -= 4

        return stats


class EvilEye(AbstractNegative):

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Luck"] -= 10

        return stats


class Curse(AbstractNegative):

    def get_stats(self):
        stats = self.base.get_stats()
        for k in stats.keys():
            if k in self.BASE_TESTIMONIAL:
                stats[k] -= 2

        return stats


def print_hero(hero):
    print(hero.get_stats())
    print(hero.get_positive_effects())
    print(hero.get_negative_effects())


if __name__ == '__main__':
    hero = Hero()
    print_hero(hero)

    berserkHero = Berserk(hero)
    print_hero(berserkHero)

    blessingHero = Blessing(berserkHero)
    print_hero(blessingHero)

    weaknessHero = Weakness(blessingHero)
    print_hero(weaknessHero)

    evilEyeHero = EvilEye(weaknessHero)
    print_hero(evilEyeHero)

    curseHero = Curse(evilEyeHero)
    print_hero(curseHero)

