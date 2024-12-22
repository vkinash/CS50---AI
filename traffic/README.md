At the start, I used 1 convolution layer with 34 filters, a kernel size of 3x3, and 1 max pooling layer with a size 
of 2x2. Additionally, I employed 1 hidden layer with 64 units. However, my model exhibited high loss - 3.4990 - and low 
accuracy - 5%.

Subsequently, I attempted to increase the number of filters from 32 to 64 in the convolution layer. This led to an
increase in accuracy to 75%, but it also caused an elevation in loss. I conducted experiments by varying the kernel 
size of the convolution layer and the size of the pooling layer, but these alterations resulted in decreased accuracy 
and increased losses. Consequently, I decided to increase the number of convolutional and pooling layers.

In this pursuit, I experimented with the number of convolutional and pooling layers, eventually settling on utilizing 
3 of each. In the first convolutional layer, I employed 32 filters, while the subsequent two layers used 64 filters. 
This configuration of filters yielded lower loss with greater accuracy.

For my subsequent step, I opted to modify the number of units in my hidden layer. With 64 units and the previously 
determined number of convolutional and pooling layers, the model achieved losses of 0.15 and an accuracy of 96% on 
average.

Further, I introduced additional hidden layers and adjusted the number of units. Upon comparing all the data, 
I concluded that 2 hidden layers - the first with 64 units and the second with 128 units - resulted in better losses 
and accuracy


