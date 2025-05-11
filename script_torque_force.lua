-- Скрипт для первой табилицы. Необходимо в директории со скриптом создать файл "DRIGATEL_test.fem",
-- который будет соответствовать положению d, из которого двигатель начнет движение против часовой стрелки.
-- Если надо в другую сторону крутить - у geom_step в определении поставить "-"

-- Результатом будет "test_table.csv", который окажется в той же директории 

-- ПАРАМЕТРЫ:
-- Вписать свой угол dq (геометрических градусов)
dq_angle = 15

showconsole()
clearconsole()

femm_dir = "./"
open(femm_dir .. "DRIGATEL_test.fem")
mi_saveas(femm_dir .. "temp.fem")
mi_seteditmode("group")

log_file = openfile("test_table.csv", "w")
write(log_file, 'Angle' .. "," .. 'Torque' .. "," .. 'Force')
write(log_file, '\n')

steps = 30
geom_step = dq_angle / steps
electric_step = 180 / steps
current_angle = 0

for n = 0, steps do
    print("--------------------")
    print("Angle: ", current_angle)

    mi_analyze(1)
    mi_loadsolution()

    -- mo_resize(1200,1000)
    -- mo_zoomnatural()
    -- mo_showcontourplot(19,-0.005,0.005,real) --19 contour lines, -0.01 to 0.1
    -- mo_showdensityplot(1,0,2.1,0,"bmag") --colour flux density plot, 0 to 2.1T
    -- filename = "images/" .. n .. ".bmp"
    -- mo_savebitmap(filename)

    mo_selectblock(0, 33)
    torque = mo_blockintegral(22)
    force_x = mo_blockintegral(18)
    force_y = mo_blockintegral(19)
    force_norm = ((force_x * force_x) + (force_y * force_y)) ^ 0.5

    print("Torque, N*m: ", torque)
    print("Force, N(A): ", force_norm)
    print("Force_X, N(A): ", force_x)
    print("Force_Y, N(A): ", force_y)

    write(log_file, current_angle .. "," .. torque .. "," .. force_norm)
    write(log_file, '\n')

    mo_close()

    mi_selectgroup(1)
    mi_moverotate(0, 0, geom_step)
    current_angle = current_angle + electric_step
end

closefile(log_file)

mi_close()