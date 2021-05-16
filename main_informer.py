import torch

from exp.exp_informer import Exp_Informer as Exp
from presettings.ett import args
print(args.freq)

print('Args in experiment:')
print(args)

for ii in range(args.itr):
    # setting_identifier record of experiments
    format_list = [args.model, args.data, args.features, args.seq_len, args.label_len, args.pred_len, args.d_model, args.n_heads,
                   args.e_layers, args.d_layers, args.d_ff, args.attn, args.factor, args.embed, args.distil, args.mix, args.des, ii]
    setting_identifier = '{}_{}_ft{}_sl{}_ll{}_pl{}_dm{}_nh{}_el{}_dl{}_df{}_at{}_fc{}_eb{}_dt{}_mx{}_{}_{}'.format(
        *format_list)

    exp = Exp(args)  # set experiments
    print('>>>>>>>start training : {}>>>>>>>>>>>>>>>>>>>>>>>>>>'.format(
        setting_identifier))
    exp.train(setting_identifier)

    print('>>>>>>>testing : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(
        setting_identifier))
    exp.test(setting_identifier)

    if args.do_predict:
        print('>>>>>>>predicting : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(
            setting_identifier))
        exp.predict(setting_identifier, True)

    torch.cuda.empty_cache()
