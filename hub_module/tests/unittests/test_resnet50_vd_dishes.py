# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import unittest

import cv2
import numpy as np
import paddle.fluid as fluid
import paddlehub as hub

pic_dir = '../image_dataset/classification/dish/'


class TestResNet50vdDish(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        """Prepare the environment once before execution of all tests.\n"""
        self.dish_classify = hub.Module(name="resnet50_vd_dishes")

    @classmethod
    def tearDownClass(self):
        """clean up the environment after the execution of all tests.\n"""
        self.dish_classify = None

    def setUp(self):
        "Call setUp() to prepare environment\n"
        self.test_prog = fluid.Program()

    def tearDown(self):
        "Call tearDown to restore environment.\n"
        self.test_prog = None

    def test_context(self):
        self.dish_classify.context(pretrained=True)

    def test_single_pic(self):
        with fluid.program_guard(self.test_prog):
            pics_path_list = [
                os.path.join(pic_dir, f) for f in os.listdir(pic_dir)
            ]
            print('\n')
            for pic_path in pics_path_list:
                print(pic_path)
                result = self.dish_classify.classification(
                    paths=[pic_path], use_gpu=False)
                print(result)

    def test_batch(self):
        with fluid.program_guard(self.test_prog):
            pics_path_list = [
                os.path.join(pic_dir, f) for f in os.listdir(pic_dir)
            ]
            print('\n')
            result = self.dish_classify.classification(
                paths=pics_path_list, batch_size=3, use_gpu=False)
            print(result)

    def test_ndarray(self):
        with fluid.program_guard(self.test_prog):
            pics_path_list = [
                os.path.join(pic_dir, f) for f in os.listdir(pic_dir)
            ]
            pics_ndarray = list()
            print('\n')
            for pic_path in pics_path_list:
                im = cv2.cvtColor(cv2.imread(pic_path), cv2.COLOR_BGR2RGB)
                result = self.dish_classify.classification(
                    images=np.expand_dims(im, axis=0), use_gpu=False)
                print(result)

    def test_save_inference_model(self):
        with fluid.program_guard(self.test_prog):
            self.dish_classify.save_inference_model(
                dirname='resnet50_vd_dishes',
                model_filename='model',
                combined=True)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestResNet50vdDish('test_context'))
    suite.addTest(TestResNet50vdDish('test_single_pic'))
    suite.addTest(TestResNet50vdDish('test_batch'))
    suite.addTest(TestResNet50vdDish('test_ndarray'))
    suite.addTest(TestResNet50vdDish('test_save_inference_model'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
