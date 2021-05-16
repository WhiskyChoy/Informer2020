from presettings.cuda_preset import args

args.freq = 'h'
args.features = 'S'
args.seq_len = 128
args.label_len = 72
args.pred_len = 36
args.enc_in = 1 # Necessary, Changes considering feature width
args.dec_in = 1 # Necessary, Changes considering feature width
args.c_out = 1 # Necessary, Changes considering feature width
args.d_model = 512
args.d_ff = 2048
args.itr = 1
args.batch_size = 64
args.train_epochs = 10
args.learning_rate = 0.0001
args.scale = True
args.test_recover = False
# args.dropout = 0.25
args.data = 'custom' # Necessary
# args.target = 'cumulative_total_deaths' # Necessary, but weird. As described in the paper, if we use 'M' we don't need to set the target
args.target = 'daily_new_deaths' # Necessary, but weird. As described in the paper, if we use 'M' we don't need to set the target
args.root_path = './covid_data/cache/pandemic_before'
args.data_path = 'Italy.csv'