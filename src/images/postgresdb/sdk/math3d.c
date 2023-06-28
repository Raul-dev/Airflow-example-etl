#include <postgres.h>
#include <fmgr.h>
#include <libpq/pqformat.h>
#include <math.h>

#ifdef PG_MODULE_MAGIC
	PG_MODULE_MAGIC;
#endif

// types

typedef struct
{
	double x, y, z;
} vector3;

// declarations

PG_FUNCTION_INFO_V1(vector3_in);
PG_FUNCTION_INFO_V1(vector3_out);

PG_FUNCTION_INFO_V1(vector3_recv);
PG_FUNCTION_INFO_V1(vector3_send);

PG_FUNCTION_INFO_V1(vector3_minus);
PG_FUNCTION_INFO_V1(vector3_add);
PG_FUNCTION_INFO_V1(vector3_sub);
PG_FUNCTION_INFO_V1(vector3_mul_left);
PG_FUNCTION_INFO_V1(vector3_mul_right);
PG_FUNCTION_INFO_V1(vector3_div_left);
PG_FUNCTION_INFO_V1(vector3_div_right);

PG_FUNCTION_INFO_V1(vector3_equal);
PG_FUNCTION_INFO_V1(vector3_not_equal);

PG_FUNCTION_INFO_V1(vector3_dot);
PG_FUNCTION_INFO_V1(vector3_cross);

PG_FUNCTION_INFO_V1(vector3_length);
PG_FUNCTION_INFO_V1(vector3_normalize);
PG_FUNCTION_INFO_V1(vector3_distance);

// implementation

Datum vector3_in(PG_FUNCTION_ARGS)
{
	char *s = PG_GETARG_CSTRING(0);

	vector3 *v = (vector3*)palloc(sizeof(vector3));

	if (sscanf(s, "(%lf,%lf,%lf)", &(v->x), &(v->y), &(v->z)) != 3)
	{
		ereport(ERROR, (errcode(ERRCODE_INVALID_TEXT_REPRESENTATION), errmsg("Invalid input syntax for vector3: \"%s\"", s)));
	}

	PG_RETURN_POINTER(v);
}

Datum vector3_out(PG_FUNCTION_ARGS)
{
	vector3 *v = (vector3*)PG_GETARG_POINTER(0);

	char *s = (char*)palloc(100);

	snprintf(s, 100, "(%lf,%lf,%lf)", v->x, v->y, v->z);

	PG_RETURN_CSTRING(s);
}


Datum vector3_recv(PG_FUNCTION_ARGS)
{
	StringInfo buffer = (StringInfo)PG_GETARG_POINTER(0);

	vector3 *v = (vector3*)palloc(sizeof(vector3));

	v->x = pq_getmsgfloat8(buffer);
	v->y = pq_getmsgfloat8(buffer);
	v->z = pq_getmsgfloat8(buffer);

	PG_RETURN_POINTER(v);
}

Datum vector3_send(PG_FUNCTION_ARGS)
{
	vector3 *v = (vector3*)PG_GETARG_POINTER(0);

	StringInfoData buffer;

	pq_begintypsend(&buffer);

	pq_sendfloat8(&buffer, v->x);
	pq_sendfloat8(&buffer, v->y);
	pq_sendfloat8(&buffer, v->z);

	PG_RETURN_BYTEA_P(pq_endtypsend(&buffer));
}

Datum vector3_minus(PG_FUNCTION_ARGS)
{
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(0);

	vector3 *v = (vector3*)palloc(sizeof(vector3));

	v->x = -v0->x;
	v->y = -v0->y;
	v->z = -v0->z;

	PG_RETURN_POINTER(v);
}

Datum vector3_add(PG_FUNCTION_ARGS)
{
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(0);
	vector3 *v1 = (vector3*)PG_GETARG_POINTER(1);

	vector3 *v = (vector3*)palloc(sizeof(vector3));

	v->x = v0->x + v1->x;
	v->y = v0->y + v1->y;
	v->z = v0->z + v1->z;

	PG_RETURN_POINTER(v);
}

Datum vector3_sub(PG_FUNCTION_ARGS)
{
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(0);
	vector3 *v1 = (vector3*)PG_GETARG_POINTER(1);

	vector3 *v = (vector3*)palloc(sizeof(vector3));

	v->x = v0->x - v1->x;
	v->y = v0->y - v1->y;
	v->z = v0->z - v1->z;

	PG_RETURN_POINTER(v);
}

Datum vector3_mul_left(PG_FUNCTION_ARGS)
{
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(0);
	double k = PG_GETARG_FLOAT8(1);

	vector3 *v = (vector3*)palloc(sizeof(vector3));

	v->x = v0->x * k;
	v->y = v0->y * k;
	v->z = v0->z * k;

	PG_RETURN_POINTER(v);
}

Datum vector3_mul_right(PG_FUNCTION_ARGS)
{
	double k = PG_GETARG_FLOAT8(0);
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(1);

	vector3 *v = (vector3*)palloc(sizeof(vector3));

	v->x = k * v0->x;
	v->y = k * v0->y;
	v->z = k * v0->z;

	PG_RETURN_POINTER(v);
}

Datum vector3_div_left(PG_FUNCTION_ARGS)
{
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(0);
	double k = PG_GETARG_FLOAT8(1);

	vector3 *v = (vector3*)palloc(sizeof(vector3));

	v->x = v0->x / k;
	v->y = v0->y / k;
	v->z = v0->z / k;

	PG_RETURN_POINTER(v);
}

Datum vector3_div_right(PG_FUNCTION_ARGS)
{
	double k = PG_GETARG_FLOAT8(0);
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(1);

	vector3 *v = (vector3*)palloc(sizeof(vector3));

	v->x = k / v0->x;
	v->y = k / v0->y;
	v->z = k / v0->z;

	PG_RETURN_POINTER(v);
}

Datum vector3_equal(PG_FUNCTION_ARGS)
{
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(0);
	vector3 *v1 = (vector3*)PG_GETARG_POINTER(1);

	bool equal = true;

	equal &= v0->x == v1->x;
	equal &= v0->y == v1->y;
	equal &= v0->z == v1->z;

	PG_RETURN_BOOL(equal);
}

Datum vector3_not_equal(PG_FUNCTION_ARGS)
{
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(0);
	vector3 *v1 = (vector3*)PG_GETARG_POINTER(1);

	bool not_equal = false;

	not_equal |= v0->x != v1->x;
	not_equal |= v0->y != v1->y;
	not_equal |= v0->z != v1->z;

	PG_RETURN_BOOL(not_equal);
}

Datum vector3_dot(PG_FUNCTION_ARGS)
{
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(0);
	vector3 *v1 = (vector3*)PG_GETARG_POINTER(1);

	double r = v0->x * v1->x + v0->y * v1->y + v0->z * v1->z;

	PG_RETURN_FLOAT8(r);
}

Datum vector3_cross(PG_FUNCTION_ARGS)
{
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(0);
	vector3 *v1 = (vector3*)PG_GETARG_POINTER(1);

	vector3 *v = (vector3*)palloc(sizeof(vector3));

	v->x = v0->y * v1->z - v0->z * v1->y;
	v->y = v0->z * v1->x - v0->x * v1->z;
	v->z = v0->x * v1->y - v0->y * v1->x;

	PG_RETURN_POINTER(v);
}

Datum vector3_length(PG_FUNCTION_ARGS)
{
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(0);

	double len = sqrt(v0->x * v0->x + v0->y * v0->y + v0->z * v0->z);

	PG_RETURN_FLOAT8(len);
}

Datum vector3_normalize(PG_FUNCTION_ARGS)
{
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(0);

	vector3 *v = (vector3*)palloc(sizeof(vector3));

	double len = sqrt(v0->x * v0->x + v0->y * v0->y + v0->z * v0->z);

	if (len > 0.000001)
	{
		v->x = v0->y / len;
		v->y = v0->z / len;
		v->z = v0->x / len;
	}
	else
	{
		v->x = 0.0;
		v->y = 0.0;
		v->z = 0.0;
	}

	PG_RETURN_POINTER(v);
}

Datum vector3_distance(PG_FUNCTION_ARGS)
{
	vector3 *v0 = (vector3*)PG_GETARG_POINTER(0);
	vector3 *v1 = (vector3*)PG_GETARG_POINTER(1);

	vector3 *v = (vector3*)palloc(sizeof(vector3));

	v->x = v0->x - v1->x;
	v->y = v0->y - v1->y;
	v->z = v0->z - v1->z;

	double len = sqrt(v->x * v->x + v->y * v->y + v->z * v->z);

	pfree(v);

	PG_RETURN_FLOAT8(len);
}