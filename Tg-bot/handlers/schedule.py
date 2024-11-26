from handlers.start import Message, FSMContext, ReplyKeyboardRemove, CallbackQuery, MemoryStorage
from aiogram import Router, F
from models.find_contacts import *
from handlers.dict import *
from keyboards.for_days import get_kb_day
from keyboards.for_schedule import get_kb_schedule


router = Router()


@router.message(F.text == "Информация о преподавателе")
async def information(message: Message):
    await message.answer("Доступная информация о преподавателе:",reply_markup=ReplyKeyboardRemove() )
    await message.answer("Выберите опцию", reply_markup=get_kb_schedule())


@router.callback_query(F.data == "Выбрать день")
async def day(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(f'Введите нужный день:', reply_markup=get_kb_day())


@router.callback_query(F.data.in_(["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]))
async def fun_day(call: CallbackQuery):
    name_to_search = data_name_to_search.get(call.message.chat.id)
    selected_day = call.data
    results = find_day(name_to_search)
    st = ""
    p_s = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = json.loads(row[1])
            if selected_day in cleaned_row2:
                for day, pairs in cleaned_row2.items():
                    if day == selected_day:
                        p_s += day + ": \n"  +  "\n".join(pairs) + "\n"
                st += "\n" + cleaned_row1 + "\n" + p_s
            else:
                await call.message.edit_text(text="В этот день у преподавателя нет пар", reply_markup=get_kb_schedule()
                )
    else:
        call.message.edit_text(text="Ошибка", reply_markup=get_kb_schedule())
    if st != "":
        await call.message.edit_text(text=f'Расписание преподавателя: {st}', reply_markup=get_kb_schedule())


@router.callback_query(F.data == "Показать полное расписание")
async def full_week(call: CallbackQuery):
    await call.answer()
    name_to_search = data_name_to_search.get(call.message.chat.id)
    results = find_full_week(name_to_search)
    st = ""
    p_s = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = json.loads(row[1])
            for day, pairs in cleaned_row2.items():
                p_s += "\n" + day + ": " + "\n" + "\n".join(pairs) + "\n"
            st += "\n" + cleaned_row1 + "\n" + p_s
    else:
        await call.message.edit_text(f'Ошибка', reply_markup=get_kb_schedule())
    await call.message.edit_text(f'Расписание преподавателя: {st}', reply_markup=get_kb_schedule())


@router.callback_query(F.data == "Показать четную неделю")
async def week_1(call: CallbackQuery):
    await call.answer()
    name_to_search = data_name_to_search.get(call.message.chat.id)
    results = find_week1(name_to_search)
    st = ""
    p_s = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = json.loads(row[1])
            for day, pairs in cleaned_row2.items():
                for pair in pairs:
                    if "▼" in  pair or "▲" not in pair:
                        if day in p_s:
                            p_s +=  pair + "\n"
                        else:
                            p_s += "\n" + day + ": "+ "\n" + pair + "\n"
            st += "\n" + cleaned_row1 + "\n" + p_s
    else:
        await call.message.edit_text(f'Ошибка', reply_markup=get_kb_schedule())
    await call.message.edit_text(f'Расписание преподавателя: {st}', reply_markup=get_kb_schedule())


@router.callback_query(F.data == "Показать нечетную неделю")
async def week_2(call: CallbackQuery):
    await call.answer()
    name_to_search = data_name_to_search.get(call.message.chat.id)
    results = find_week2(name_to_search)
    st = ""
    p_s = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = json.loads(row[1])
            for day, pairs in cleaned_row2.items():
                for pair in pairs:
                    if "▼" not in  pair or "▲" in pair:
                        if day in p_s:
                            p_s +=  pair + "\n"
                        else:
                            p_s += "\n" + day + ": "+ "\n" + pair + "\n"
            st += "\n" + cleaned_row1 + "\n" + p_s
    else:
        await call.message.edit_text(f'Ошибка', reply_markup=get_kb_schedule())
    await call.message.edit_text(f'Расписание преподавателя: {st}', reply_markup=get_kb_schedule())


@router.callback_query(F.data == "Контакты")
async def contacts(call: CallbackQuery):
    await call.answer()
    name_to_search = data_name_to_search.get(call.message.chat.id)
    results = find_contacts(name_to_search)
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = row[1].strip()
            cleaned_row3 = row[2].strip()
            st += "\n" + cleaned_row1 + ".\nКонтакты: " + cleaned_row2 + "\n" + cleaned_row3
    else:
        await call.message.edit_text(f'Ошибка', reply_markup=get_kb_schedule())
    await call.message.edit_text(f'{st}', reply_markup=get_kb_schedule())