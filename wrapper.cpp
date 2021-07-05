#include <Python.h>
#include <math.h>
#include <stdio.h>

// https://docs.scipy.org/doc/numpy/reference/c-api/types-and-structures.html
typedef struct {
    PyObject_HEAD
    uint8_t *data;
    int nd;
    int64_t *dimensions;
    int64_t *strides;
} PyArrayObject;

#define M_PI        3.14159265358979323846

double radians(double x)
{
    return x * (M_PI / 180.0);
}

// https://python3-cookbook.readthedocs.io/zh_CN/latest/chapters/p15_c_extensions.html
static PyObject* py_get_perspective(PyObject *self, PyObject *args)
{
    PyArrayObject *input, *output, *mat;
    double fov;
    if (!PyArg_ParseTuple(args, "OOOd", &input, &output, &mat, &fov))
        return NULL;

    int iw, ih, ow, oh;
    double equ_cx, equ_cy;
    double *mat_data = (double*)mat->data;
    iw = input->dimensions[1];
    ih = input->dimensions[0];
    ow = output->dimensions[1];
    oh = output->dimensions[0];
    equ_cx = (iw - 1) / 2.0;
    equ_cy = (ih - 1) / 2.0;

    double w_len = tan(radians(fov / 2.0));
    double h_len = w_len * oh / ow;

    for(int i = 0; i < oh; i++)
    for(int j = 0; j < ow; j++)
    {
        double x, y, z, d;
        double xx, yy, zz;
        int lat, lon;
        x = -w_len + 2 * w_len / (ow - 1) * j;
        y = -h_len + 2 * h_len / (oh - 1) * i;
        z = 1;
        d = sqrt(x * x + y * y + z * z);
        x /= d;
        y /= d;
        z /= d;
        xx = mat_data[0] * x + mat_data[1] * y + mat_data[2] * z;
        yy = mat_data[3] * x + mat_data[4] * y + mat_data[5] * z;
        zz = mat_data[6] * x + mat_data[7] * y + mat_data[8] * z;
        lat = asin(yy) / M_PI * 2 * equ_cy + equ_cy;
        lon = atan2(xx, zz) / M_PI * equ_cx + equ_cx;
        output->data[(i * ow + j) * 3 + 0] = input->data[(lat * iw + lon) * 3 + 0];
        output->data[(i * ow + j) * 3 + 1] = input->data[(lat * iw + lon) * 3 + 1];
        output->data[(i * ow + j) * 3 + 2] = input->data[(lat * iw + lon) * 3 + 2];
    }

    Py_RETURN_NONE;
}

/* Module method table */
static PyMethodDef SampleMethods[] = {
  {"get_perspective", py_get_perspective, METH_VARARGS, "get_perspective"},
  { NULL, NULL, 0, NULL}
};

/* Module structure */
static struct PyModuleDef samplemodule = {
  PyModuleDef_HEAD_INIT,
  "sample",           /* name of module */
  "A sample module",  /* Doc string (may be NULL) */
  -1,                 /* Size of per-interpreter state or -1 */
  SampleMethods       /* Method table */
};

/* Module initialization function */
PyMODINIT_FUNC
PyInit_equirec2perspec(void) {
    return PyModule_Create(&samplemodule);
}
