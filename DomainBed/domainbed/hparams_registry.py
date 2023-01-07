# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import numpy as np
from domainbed.lib import misc


def _define_hparam(hparams, hparam_name, default_val, random_val_fn):
    hparams[hparam_name] = (hparams, hparam_name, default_val, random_val_fn)


def _hparams(algorithm, dataset, random_seed):
    """
    Global registry of hyperparams. Each entry is a (default, random) tuple.
    New algorithms / networks / etc. should add entries here.
    """
    SMALL_DATASET = ["ColoredMNIST_IRM", "ColoredMNIST_IRM_IID", "ColoredMNIST_IRM_Blue", "ColoredMNIST", "RotatedMNIST", "VLCS", "PACS", "OfficeHome", "TerraIncognita", "DomainNet", "SVIRO"]
    SMALL_IMAGES = ['Debug28', 'RotatedMNIST', 'ColoredMNIST', 'ColoredMNIST_RGB', 'ColoredMNIST_IRM', 'ColoredMNIST_IRM_IID', 'ColoredMNIST_IRM_Blue', 'ColoredMNIST_IRM_Div']

    hparams = {}

    def _hparam(name, default_val, random_val_fn):
        """Define a hyperparameter. random_val_fn takes a RandomState and
        returns a random hyperparameter value."""
        assert(name not in hparams)
        random_state = np.random.RandomState(
            misc.seed_hash(random_seed, name)
        )
        hparams[name] = (default_val, random_val_fn(random_state))

    # Unconditional hparam definitions.

    _hparam('data_augmentation', True, lambda r: True)
    _hparam('resnet18', False, lambda r: False)
    _hparam('resnet_dropout', 0., lambda r: r.choice([0., 0.1, 0.5]))
    _hparam('class_balanced', False, lambda r: False)
    # TODO: nonlinear classifiers disabled
    _hparam('nonlinear_classifier', False,
            lambda r: bool(r.choice([False, False])))

    # Algorithm-specific hparam definitions. Each block of code below
    # corresponds to exactly one algorithm.

    if algorithm in ['DANN', 'CDANN']:
        _hparam('lambda', 1.0, lambda r: 10**r.uniform(-2, 2))
        _hparam('weight_decay_d', 0., lambda r: 10**r.uniform(-6, -2))
        _hparam('d_steps_per_g_step', 1, lambda r: int(2**r.uniform(0, 3)))
        _hparam('grad_penalty', 0., lambda r: 10**r.uniform(-2, 1))
        _hparam('beta1', 0.5, lambda r: r.choice([0., 0.5]))
        _hparam('mlp_width', 256, lambda r: int(2 ** r.uniform(6, 10)))
        _hparam('mlp_depth', 3, lambda r: int(r.choice([3, 4, 5])))
        _hparam('mlp_dropout', 0., lambda r: r.choice([0., 0.1, 0.5]))

    elif algorithm == 'Fish':
        _hparam('meta_lr', 0.5, lambda r:r.choice([0.05, 0.1, 0.5]))

    elif algorithm == "W2D":
        _hparam('rsc_f_drop_factor', 1 / 4, lambda r: r.uniform(0.1, 0.4))
        _hparam('last_k_epoch', 1 / 4, lambda r: r.uniform(0.2, 0.4))
        if dataset in SMALL_DATASET:
            _hparam('rsc_b_drop_factor', 1 / 4, lambda r: r.uniform(0.1, 0.3))
            _hparam('worst_case_p', 1 / 3, lambda r: r.uniform(0.1, 0.5))
        else:
            _hparam('rsc_b_drop_factor', 1 / 3, lambda r: r.uniform(0.1, 0.4))
            _hparam('worst_case_p', 1 / 3, lambda r: r.uniform(0.2, 0.4))

    elif algorithm == "RSC":
        _hparam('rsc_f_drop_factor', 1 / 3, lambda r: r.uniform(0, 0.5))
        _hparam('rsc_b_drop_factor', 1 / 3, lambda r: r.uniform(0, 0.5))

    elif algorithm == "SagNet":
        _hparam('sag_w_adv', 0.1, lambda r: 10**r.uniform(-2, 1))

    elif algorithm == "IRM":
        _hparam('irm_lambda', 1e2, lambda r: 10**r.uniform(-1, 5))
        if dataset == 'CelebA_Blonde':
            _hparam('irm_penalty_anneal_iters', 500,
                    lambda r: int(10**r.uniform(0, 3.5)))
        else:
            _hparam('irm_penalty_anneal_iters', 500,
                    lambda r: int(10**r.uniform(0, 4)))

    elif algorithm == "Mixup":
        _hparam('mixup_alpha', 0.2, lambda r: 10**r.uniform(-1, -1))

    elif algorithm == "GroupDRO":
        _hparam('groupdro_eta', 1e-2, lambda r: 10**r.uniform(-3, -1))

    elif algorithm == "MMD" or algorithm == "CORAL":
        _hparam('mmd_gamma', 1., lambda r: 10**r.uniform(-1, 1))

    elif algorithm == "MLDG":
        _hparam('mldg_beta', 1., lambda r: 10**r.uniform(-1, 1))

    elif algorithm == "MTL":
        _hparam('mtl_ema', .99, lambda r: r.choice([0.5, 0.9, 0.99, 1.]))

    elif algorithm == "VREx":
        _hparam('vrex_lambda', 1e1, lambda r: 10**r.uniform(-1, 5))
        if dataset == 'CelebA_Blonde':
            _hparam('vrex_penalty_anneal_iters', 500,
                    lambda r: int(10**r.uniform(0, 3.5)))
        else:
            _hparam('vrex_penalty_anneal_iters', 500,
                    lambda r: int(10**r.uniform(0, 4)))

    elif algorithm == "SD":
        _hparam('sd_reg', 0.1, lambda r: 10**r.uniform(-5, -1))

    elif algorithm == "ANDMask":
        _hparam('tau', 1, lambda r: r.uniform(0.5, 1.))

    elif algorithm == "IGA":
        _hparam('penalty', 1000, lambda r: 10**r.uniform(1, 5))
        
    elif algorithm =="ERDG":
        _hparam('lr_d', 5e-5, lambda r: 10**r.uniform(-5, -3.5))
        _hparam('lr_c', 5e-6, lambda r: 10**r.uniform(-6, -4.5))
        _hparam('lr_cp', 5e-6, lambda r: 10**r.uniform(-6, -4.5))
        _hparam('lbd_c', 0.05, lambda r: 10**r.uniform(-3, -1))
        _hparam('lbd_cp', 0.01, lambda r: 10**r.uniform(-4, -1))
        _hparam('lbd_d', 0.5, lambda r: 10**r.uniform(-2, 0))
        
    elif algorithm == "TTT":
        _hparam('rotate_type', "expand", lambda r: r.choice(["expand","rand"]))
        _hparam('iter_num', 10, lambda r: r.choice([10,50,100]))

    # Dataset-and-algorithm-specific hparam definitions. Each block of code
    # below corresponds to exactly one hparam. Avoid nested conditionals.

    if dataset in SMALL_IMAGES:
        _hparam('lr', 1e-3, lambda r: 10**r.uniform(-4.5, -2.5))
    else:
        _hparam('lr', 5e-5, lambda r: 10**r.uniform(-5, -3.5))

    if dataset in SMALL_IMAGES:
        _hparam('weight_decay', 0., lambda r: 0.)
    else:
        _hparam('weight_decay', 0., lambda r: 10**r.uniform(-6, -2))

    if dataset in SMALL_IMAGES:
        _hparam('batch_size', 64, lambda r: int(2**r.uniform(3, 9)))
    elif algorithm == 'ARM':
        _hparam('batch_size', 8, lambda r: 8)
    elif dataset == 'DomainNet':
        _hparam('batch_size', 32, lambda r: int(2**r.uniform(3, 5)))
    elif dataset == 'CelebA_Blonde':
        _hparam('batch_size', 48, lambda r: int(2**r.uniform(4.5, 6)))
    else:
        _hparam('batch_size', 32, lambda r: int(2**r.uniform(4, 5.5)))

    if algorithm in ['DANN', 'CDANN'] and dataset in SMALL_IMAGES:
        _hparam('lr_g', 1e-3, lambda r: 10**r.uniform(-4.5, -2.5))
    elif algorithm in ['DANN', 'CDANN']:
        _hparam('lr_g', 5e-5, lambda r: 10**r.uniform(-5, -3.5))

    if algorithm in ['DANN', 'CDANN'] and dataset in SMALL_IMAGES:
        _hparam('lr_d', 1e-3, lambda r: 10**r.uniform(-4.5, -2.5))
    elif algorithm in ['DANN', 'CDANN']:
        _hparam('lr_d', 5e-5, lambda r: 10**r.uniform(-5, -3.5))

    if algorithm in ['DANN', 'CDANN'] and dataset in SMALL_IMAGES:
        _hparam('weight_decay_g', 0., lambda r: 0.)
    elif algorithm in ['DANN', 'CDANN']:
        _hparam('weight_decay_g', 0., lambda r: 10**r.uniform(-6, -2))

    return hparams


def default_hparams(algorithm, dataset):
    return {a: b for a, (b, c) in _hparams(algorithm, dataset, 0).items()}


def random_hparams(algorithm, dataset, seed):
    return {a: c for a, (b, c) in _hparams(algorithm, dataset, seed).items()}