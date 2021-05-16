from exp.exp_informer import Exp_Informer as Exp
import torch
import numpy as np
from presettings.long_fit import args
import matplotlib.pyplot as plt
from covid_data import data_handler


data_handler.generate_all_data('new', False)



# setting_identifier record of experiments
# target_country = args.data_path.split('.')[0]
# format_list = [args.model, args.data, args.features, args.seq_len, args.label_len, args.pred_len, args.d_model, args.n_heads,
#                 args.e_layers, args.d_layers, args.d_ff, args.attn, args.factor, args.embed, args.distil, args.mix, args.des, 0, target_country]
# setting_identifier = '{}_{}_ft{}_sl{}_ll{}_pl{}_dm{}_nh{}_el{}_dl{}_df{}_at{}_fc{}_eb{}_dt{}_mx{}_{}_{}_{}_long'.format(
#     *format_list)

# exp = Exp(args)  # set experiments
# print('>>>>>>>start training : {}>>>>>>>>>>>>>>>>>>>>>>>>>>'.format(
#     setting_identifier))
# exp.train(setting_identifier)

# print('>>>>>>>testing : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(
#     setting_identifier))
# exp.test(setting_identifier)

# print('>>>>>>>predicting : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(
#     setting_identifier))
# exp.predict(setting_identifier, True)

# # setting_identifier = 'informer_custom_ftS_sl128_ll72_pl36_dm512_nh8_el2_dl1_df2048_atprob_fc5_ebtimeF_dtTrue_mxTrue_test_0_Italy'

# preds = np.load('./results/'+setting_identifier+'/pred.npy')
# trues = np.load('./results/'+setting_identifier+'/true.npy')
# # print(trues[0,:,:])
# plt.figure()
# plt.plot(trues[0,:,0], label='GroundTruth')
# plt.plot(preds[0,:,0], label='Prediction')
# plt.legend()
# plt.show()
# # for i in range(1, 60):
# #     print(i)
# #     plt.figure()
# #     plt.plot(trues[i,:,0], label='GroundTruth')
# #     plt.plot(preds[i,:,0], label='Prediction')
# #     plt.legend()
# #     plt.show()
# torch.cuda.empty_cache()
