import sys

sys.path.append("..\\..\\auto_CoA")

from module.save.local_storage import LocalStorageMgr

test_int = 42
test_float = 3.14
test_bool = True
test_str = "test"
test_list = [1, 2, 3]
test_tuple = (4, 5, 6)
test_set = {7, 8, 9}
test_dict = {"a": 1, "b": 2, "c": 3}

ls = LocalStorageMgr().getLocalStorage()
ls.set_item("test_int", test_int)
ls.set_item("test_float", test_float)
ls.set_item("test_bool", test_bool)
ls.set_item("test_str", test_str)
ls.set_item("test_list", test_list)
ls.set_item("test_tuple", test_tuple)
# ls.set_item("test_set", test_set) 不支持set类型
ls.set_item("test_dict", test_dict)

print(ls.get_item("test_int"))
print(ls.get_item("test_float"))
print(ls.get_item("test_bool"))
print(ls.get_item("test_str"))
print(ls.get_item("test_list"))
print(ls.get_item("test_tuple"))
print(ls.get_item("test_set"))
print(ls.get_item("test_dict"))
print(ls.get_item("test"))

print("------------")
ls.remove_item("test_int")
print(ls.get_item("test_int"))

print("------------")
ls.clear()
print(ls.get_item("test_str"))
