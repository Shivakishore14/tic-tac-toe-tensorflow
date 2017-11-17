import Input
import Model

input_Data = Input.Input()
input_Data.readFromFile()
input_Data.processData()
x, y = input_Data.getData()

model = Model.Model()

model.model(9,9)
model.model_train_init(x,y,10000)
model.test(x,y)

model.model_train_new(x,y,1000)
model.test(x,y)
print model.predict(x)
