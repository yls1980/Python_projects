# -*- coding: utf-8 -*-

# Вывести на консоль жителей комнат (модули room_1 и room_2)
# Формат: В комнате room_1 живут: ...
from lesson_005 import room_1, room_2

# Нужно вывести жителей, а не их количество.
print("В комнате room_1 живут: %s" % (', '.join(room_1.folks)))
print("В комнате room_2 живут: %s" % (', '.join(room_2.folks)))

# Зачёт!
