#!/usr/bin/env python3

from __future__ import division, print_function

import sys
import argparse

import pyglet
import numpy as np

import gym
import gym_duckietown
from gym_duckietown.envs import SimpleSimEnv

parser = argparse.ArgumentParser()
parser.add_argument('--env-name', default='SimpleSim-v0')
parser.add_argument('--draw-curve', action='store_true')
args = parser.parse_args()

if args.env_name == 'SimpleSim-v0':
    env = SimpleSimEnv(draw_curve=args.draw_curve)
else:
    env = gym.make(args.env_name)

env.reset()
env.render()

def save_numpy_img(file_name, img):
    img = np.ascontiguousarray(img)
    img = (img * 255).astype(np.uint8)
    img = np.flip(img, 0)

    from skimage import io
    io.imsave(file_name, img)

lastImgNo = 0
def save_img(img):
    global lastImgNo
    save_numpy_img('img_%03d.png' % lastImgNo, img)
    lastImgNo += 1

avg_reward = 0

@env.window.event
def on_key_press(symbol, modifiers):
    from pyglet.window import key

    action = None
    if symbol == key.LEFT:
        print('left')
        action = np.array([0.00, 0.40])
    elif symbol == key.RIGHT:
        print('right')
        action = np.array([0.40, 0.00])
    elif symbol == key.UP:
        print('forward')
        action = np.array([0.40, 0.40])
    elif symbol == key.SLASH:
        print('RESET')
        action = None
        env.reset()
        env.render()
    elif symbol == key.SPACE:
        action = np.array([0, 0])
    elif symbol == key.ESCAPE:
        env.close()
        sys.exit(0)
    else:
        return

    if action is not None:
        print('stepping')
        obs, reward, done, info = env.step(action)
        avg_reward = 0.99*avg_reward + 0.01*reward
        print('step_count = %s, reward=%.3f, avg_reward=%.3f\n' % (env.step_count, reward, avg_reward))

        env.render()

        #save_img(obs)

        if done:
            print('done!')
            env.reset()
            env.render()

# Enter main event loop
pyglet.app.run()

env.close()
