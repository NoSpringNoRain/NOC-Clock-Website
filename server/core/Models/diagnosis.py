## Dementia diagnosis, Boston University 2021

###
# Imports
###
import joblib
import argparse

import cv2 as cv
import numpy as np
import os.path as osp

import tensorflow as tf
from tensorflow import keras

import os
import warnings
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# Defining the CLI via argument parsing
def cli(n_folds, max_age=150):
  ''' command line interface:
  Inputs: n_folds(int) - # of folds for. restricts choices of --fold argument
           max_age(int) - restrits choices for --age argument
  Output: parsed arguments
  '''
  description = 'Prediction: dementia diagnosis using clock drawing and age'
  prog = '%(prog)s'
  optional_args_usage = f' [-h] [-f {{0...{n_folds}}}] [-a {{0...{max_age-1}}}]'
  positional_args_usage = f' clk_img_path'
  usage =  prog + optional_args_usage + positional_args_usage

  argparser = argparse.ArgumentParser(description=description, usage=usage)

  # adding arguments to parse
  # 1) fold (optional argument) - default: 0, type: int, range: (0, n_folds)
  argparser.add_argument('-f', '--fold', type=int, 
            choices=range(n_folds), default=0,
            metavar='FOLD',
            help='fold number used to load model and input normalization')

  # 2) age (optional arguement) - default: None, tyoe: int, range: (0, max_age)
  argparser.add_argument('-a', '--age', type=int, 
                        choices=range(max_age), default=None,
                        metavar='AGE', help='patient age')
  
  # 3) clk_img_path (positional argument) - type: string, path to clock image
  argparser.add_argument('clk_img_path', type=str, help='path to clock img')

  # parse arguments and return
  return argparser.parse_args()

def preprocess(img, dim=128, n=255.0): 
  ''' takes the input image and performs the following pre-processing
  assumes 2d grayscale image and removes all other channel if it exists
  1) resizes image to img_dim dimensions 
  2) normalizes input image pixels by factor n
  Input: img (cv image)
         img_dim (int) : used to resize input image, default-128X128
         n (float): factor used to normalize image pixels
  Output: preprocessed image (np array)
  '''
  square = cv.resize(img, (dim, dim))
  norm = np.array(square, dtype=np.float)/n
  return norm

def z_norm(x, mu, std):
  if x is not None:
    return (x-mu)/std
  else: return None

def main():
  # Project parameters
  n_folds = 5
  norm_params = {
    'cmd_score': {
      'mean' : [0.22, 0.20, 0.26, 0.26, 0.29],
      'std' : [0.25, 0.21, 0.25, 0.24, 0.26],
    },
    'age' : {
      'mean' : [63.68, 63.68, 63.68, 63.68, 63.68],
      'std' : [13.59, 13.59, 13.59, 13.59, 13.59],
    }
  }

  # model paths
  cnn_cmd_clk_mdl_paths = [f'./core/Models/model_cmd{i}/' for i in range(n_folds)]
  logreg_mdl_paths = [f'./core/Models/regression_f{i}.sav' for i in range(n_folds)]
  logreg_mdl_paths_a = [f'./core/Models/regression_age_cmd_f{i}.sav' for i in range(n_folds)]
  
  # arg parsing through the cli
  args = cli(n_folds=n_folds)

  # Input processing 
  fold = args.fold
  age = args.age
  clk_img_path = args.clk_img_path

  # redundant parameter checks (usually handled by argparser)
  assert fold in range(n_folds)
  if age is not None: assert isinstance(age, int)

  # check if image path exists and if it does, try openign the img
  if osp.exists(clk_img_path):
    try:
      clk_img = cv.imread(clk_img_path)
      if clk_img is not None: clk_img = preprocess(clk_img)
      else: print('Error: Invalid image. Input image is empty')
    except Exception: print(f'Unable to open and preprocess image: {clk_img_path}')
  else: print(f'{clk_img_path} does not exist, provide a valid image path')

  cmd_score_mu, cmd_score_std = norm_params['cmd_score']['mean'][fold], norm_params['cmd_score']['std'][fold]
  age_mu, age_std = norm_params['age']['mean'][fold], norm_params['age']['std'][fold]

  # loading trained models
  cnn_clk_mdl = cnn_cmd_clk_mdl_paths[fold]
  logreg_mdl = logreg_mdl_paths_a[fold] if age is not None else logreg_mdl_paths[fold]

  cmd_clock_cnn = keras.models.load_model(cnn_clk_mdl)
  logreg = joblib.load(logreg_mdl)

  # make predictions using loaded model
  cmd_score = cmd_clock_cnn.predict(np.array([clk_img]))


  print(cmd_score[0][0])
  # # age_ = z_norm(age, age_mu, age_std)
  # # cmd_score_ = z_norm(cmd_score, cmd_score_mu, cmd_score_std)
  # diagnosis = logreg.predict_proba(np.asarray([age_, cmd_score_])) if age is not None else logreg.predict_proba(np.asarray(cmd_score))
  diagnosis = cmd_score[0][0]
  return diagnosis

if __name__=='__main__':
  diagnosis = main()