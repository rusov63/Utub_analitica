import unittest
from utils.class_channel import Channel, Video, PLVideo
class TestChannel(unittest.TestCase):

    def test__init__(self):
        id1 = 'UCMCgOm8GZkHp8zJ6l7_hIuA'
        id2 = 'UC1eFXmJNkjITxPFWTy6RsWg'
        assert id1 == 'UCMCgOm8GZkHp8zJ6l7_hIuA'
        assert id2 == 'UC1eFXmJNkjITxPFWTy6RsWg'
    def test__str__(self):
        """Тест на проверку ID канала"""
        id1 = 'UCMCgOm8GZkHp8zJ6l7_hIuA'
        id2 = 'UC1eFXmJNkjITxPFWTy6RsWg'
        assert id1.__str__() == 'UCMCgOm8GZkHp8zJ6l7_hIuA'
        assert id2.__str__() == 'UC1eFXmJNkjITxPFWTy6RsWg'

    def test__lt__(self):
        """сравнение каналов ">" на количество подписчиков"""
        ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
        ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
        assert ch1.__lt__(ch2) is False

    def test__gt__(self):
        """сравнение каналов "<" на количество подписчиков"""
        ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
        ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
        assert ch1.__gt__(ch2) is True
    def test__add__(self):
        """Общее количество подписчиков """
        ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
        ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
        assert ch1.__add__(ch2) == 14000000

class TestVideo(unittest.TestCase):
    def test__str__(self):
        video1 = Video('9lO06Zxhu88')
        video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
        assert video1.__str__() == 'Как устроена IT-столица мира / Russian Silicon Valley (English subs)'
        assert video2.__str__() == 'Пушкин: наше все?'
