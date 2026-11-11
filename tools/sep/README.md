# Spleeter 5-stem separation without TensorFlow (numpy, checked against the published ONNX 2-stem model to 0.02%).
# Weights: https://github.com/deezer/spleeter/releases/download/v1.4.0/5stems.tar.gz (unpack to dl/s5). 5stems is softmax_unet with ELU:
#   import unet as U; U.ACT["enc"] = U.ACT["dec"] = U.elu; E = U.softmax_unet(M, load("dl/s5/model"), 5)  # vocals, piano, drums, bass, other
# M: |STFT| (hann 4096, hop 1024, scaled x2048 like tf.signal.stft), first 1024 bins, chunks of 512 frames, (512, 1024, 2).
