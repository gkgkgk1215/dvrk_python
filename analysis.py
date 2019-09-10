"""Analyze pickle files. REQUIRES PYTHON 2.7 (sorry). Call like this:

`python analysis.py`

with `results` file in the correct path.

NOTES:

The only episodes which I think have issues with lengths of the lists is tier1,
color, episode 000, which has duplicate coverage.

The number of actions should be one less than the number of images and coverage
statistics.

At some point on September 6, I made the episode length 10.

Starting September 8 and beyond for the last week:
  - Follow protocol of starting the cloth, then randomizing which of RGB or
    depth is applied. Then we recreate the cloth as close as we can, and do the
    other experiment.
  - We use the de-noising that Ryan Hoque suggested.

Starting September 9, I'm using a lighter blue cloth, which should more closely
match what we have in simulation.
"""
import os
import cv2
import sys
import pickle
import time
import numpy as np
np.set_printoptions(precision=4, linewidth=200)
from os.path import join
from collections import defaultdict


def _criteria(x, MONTH_BEGIN=9, DAY_BEGIN=6):
    """Filter older entries, `x` is full path.

    I started on the 6th but changed the protocol a bit afterwards.
    """

    # Get only the pickle file name.
    x = os.path.basename(x)

    # Handle first few cases without date.
    assert x[-4:] == '.pkl', x
    x = x[:-4]  # remove `.pkl`
    ss = x.split('_')
    assert ss[0] == 'ep', ss

    if len(ss) == 2:
        # Then this was saved without a date. Only include if 'day begin' was 6.
        return DAY_BEGIN == 6
    else:
        date = (ss[2]).split('-')
        assert len(date) == 5, date
        year, month, day = int(date[0]), int(date[1]), int(date[2])
        assert year == 2019, year
        assert month == 9, month
        #print(x, date, year, month, day, day >= DAY_BEGIN)
        begin = day >= DAY_BEGIN
        return begin


def analyze_single(pth, episode_idx=None):
    target = 'tmp'
    with open(pth, 'r') as fh:
        data = pickle.load(fh)
    print('coverage: {}'.format(data['coverage']) )
    print('coverage len: {}'.format(len(data['coverage'])))
    print('c_img len:    {}'.format(len(data['c_img'])))
    print('d_img len:    {}'.format(len(data['d_img'])))
    print('actions len:  {}'.format(len(data['actions'])))
    for idx,(c_img,d_img) in enumerate(zip(data['c_img'], data['d_img'])):
        pth_c = join(target,'c_img_{}.png'.format(idx))
        pth_d = join(target,'d_img_{}.png'.format(idx))
        cv2.imwrite(pth_c, c_img)
        cv2.imwrite(pth_d, d_img)


def analyze_group(head):
    """Go through all experiments of a certain condition."""
    ep_files = sorted([join(head,x) for x in os.listdir(head) if x[-4:]=='.pkl'])
    ss = defaultdict(list)
    num_counted = 0

    for ep in ep_files:
        if not _criteria(ep):
            print('SKIPPING {}; it is an older trial.'.format(ep))
            continue
        num_counted += 1

        print('{}'.format(ep))
        with open(ep, 'r') as fh:
            data = pickle.load(fh)
        print('  coverage len {}, and values:   {}'.format(len(data['coverage']),
                    np.array(data['coverage'])))
        print('  c,d_img len: {} {}'.format(len(data['c_img']), len(data['d_img'])))
        print('  actions len: {}'.format(len(data['actions'])))
        print('  max/min/avg/start/end: {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}'.format(
                np.max(data['coverage']), np.min(data['coverage']),
                np.mean(data['coverage']), data['coverage'][0],
                data['coverage'][-1])
        )
        # WAIT --- I think we want max/min/avg AFTER the starting coverage!
        ss['max'].append( np.max(data['coverage'][1:]) )
        ss['min'].append( np.min(data['coverage'][1:]) )
        ss['avg'].append( np.mean(data['coverage'][1:]) )
        ss['beg'].append( data['coverage'][0] )
        ss['end'].append( data['coverage'][-1] )

    # Multiply by 100 :-)
    for key in ss.keys():
        ss[key] = np.array(ss[key]) * 100
    print('\nOverall stats across {} trials:'.format(num_counted))
    print('start: {:.1f} +/- {:.1f}'.format(np.mean(ss['beg']), np.std(ss['beg'])) )
    print('end:   {:.1f} +/- {:.1f}'.format(np.mean(ss['end']), np.std(ss['end'])) )
    print('max:   {:.1f} +/- {:.1f}'.format(np.mean(ss['max']), np.std(ss['max'])) )
    print('min:   {:.1f} +/- {:.1f}'.format(np.mean(ss['min']), np.std(ss['min'])) )
    print('avg:   {:.1f} +/- {:.1f}'.format(np.mean(ss['avg']), np.std(ss['avg'])) )

    # In readable format for LaTeX:
    _str = '& {:.1f} +/- {:.1f} & {:.1f} +/- {:.1f} & {:.1f} +/- {:.1f} & {:.1f} +/- {:.1f} \\\\'.format(
            np.mean(ss['beg']),np.std(ss['beg']),
            np.mean(ss['end']),np.std(ss['end']),
            np.mean(ss['max']),np.std(ss['max']),
            np.mean(ss['avg']),np.std(ss['avg']),
    )
    #print(_str)
    return _str, num_counted


if __name__ == "__main__":
    #pth = join('results','tier1_color','ep_000.pkl')
    #analyze_single(pth)

    # Analyze.
    print('\n*********************************************')
    print('ANALYZING TIER 1 COLOR')
    print('*********************************************\n')
    head = join('results', 'tier1_color')
    str1, nb1 = analyze_group(head)

    print('\n*********************************************')
    print('ANALYZING TIER 1 DEPTH')
    print('*********************************************\n')
    head = join('results', 'tier1_depth')
    str2, nb2 = analyze_group(head)

    print('\n*********************************************')
    print('ANALYZING TIER 2 COLOR')
    print('*********************************************\n')
    head = join('results', 'tier2_color')
    str3, nb3 = analyze_group(head)

    print('\n*********************************************')
    print('ANALYZING TIER 2 DEPTH')
    print('*********************************************\n')
    head = join('results', 'tier2_depth')
    str4, nb4 = analyze_group(head)

    print('\n*********************************************')
    print('ANALYZING TIER 3 COLOR')
    print('*********************************************\n')
    head = join('results', 'tier3_color')
    str5, nb5 = analyze_group(head)

    print('\n*********************************************')
    print('ANALYZING TIER 3 DEPTH')
    print('*********************************************\n')
    head = join('results', 'tier3_depth')
    str6, nb6 = analyze_group(head)

    print('\nNumber of trials we record:')
    print(nb1, nb2, nb3, nb4, nb5, nb6)
    print('\n\nCopy and paste this for LaTeX:\nstart, end, max, mean')
    print('T1 RGB  '+ str1)
    print('T1 Dep. '+ str2)
    print('T2 RGB  '+ str3)
    print('T2 Dep. '+ str4)
    print('T3 RGB  '+ str5)
    print('T3 Dep. '+ str6)
