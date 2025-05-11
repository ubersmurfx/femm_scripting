-- Скрипт для второй таблицы. Необходимо в директории со скриптом создать файл "DRIGATEL_interswitch.fem",
-- который будет соответствовать положению dq

-- Результатом будет "interswitch_table.csv", который окажется в той же директории 

-- ПАРАМЕТРЫ:
-- Вводим свою площадь сектора обмотки (мм2)
sector_area = 72.31
-- Вводим точку на зубце статора, где хотим мерять Индукцию
stator_x = -3.3
stator_y = 45.9


showconsole()
clearconsole()

femm_dir = "./"
open(femm_dir .. "rotate_work_posDQ.fem")
mi_saveas(femm_dir .. "interswitch_temp.fem")

log_file = openfile("interswitch_table.csv", "w")
write(log_file, 'Density' .. "," .. 'Torque' .. "," .. 'Force' .. "," .. 'Induction')
write(log_file, '\n')

current = 0
current_density = 0
density_step = 5
steps = 20

for n = 0, steps do
    mi_modifycircprop("A+", 1, current)
    mi_modifycircprop("A-", 1, -current)

    print("--------------------")
    print("Density: ", current_density)

    mi_analyze(0)
    mi_loadsolution()

    A, B_X, B_Y, Sig, E, H1, H2, Je, Js, Mu1, Mu2, Pe, Ph = mo_getpointvalues(stator_x, stator_y)
    B_norm = ((B_X * B_X) + (B_Y * B_Y)) ^ 0.5

    mo_selectblock(0, 33)
    torque = mo_blockintegral(22)
    force_x = mo_blockintegral(18)
    force_y = mo_blockintegral(19)
    force_norm = ((force_x * force_x) + (force_y * force_y)) ^ 0.5

    print("Torque, N*m: ", torque)
    print("Force, N(A): ", force_norm)
    print("Inductivity, T: ", B_norm)
    print("Force_X, N(A): ", force_x)
    print("Force_Y, N(A): ", force_y)
    print("Inductivity_X, T: ", B_X)
    print("Inductivity_Y, T: ", B_Y)

    write(log_file, current_density .. "," .. torque .. "," .. force_norm .. "," .. B_norm)
    write(log_file, '\n')

    mo_close()

    current_density = current_density + density_step
    current = current_density * 0.33 * sector_area
    if n == 9 then density_step = 10 end
end

closefile(log_file)

mi_close()