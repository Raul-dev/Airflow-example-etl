CREATE TYPE vector3;

CREATE OR REPLACE FUNCTION vector3_in ( s cstring )
RETURNS vector3 AS
'MODULE_PATHNAME', 'vector3_in'
LANGUAGE C IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION vector3_out ( v vector3 )
RETURNS cstring AS
'MODULE_PATHNAME', 'vector3_out'
LANGUAGE C IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION vector3_recv ( p internal )
RETURNS vector3 AS
'MODULE_PATHNAME', 'vector3_recv'
LANGUAGE C IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION vector3_send ( v vector3 )
RETURNS bytea AS
'MODULE_PATHNAME', 'vector3_send'
LANGUAGE C IMMUTABLE STRICT;

CREATE TYPE vector3
(
	internallength = 24,
	input = vector3_in,
	output = vector3_out,
	receive = vector3_recv,
	send = vector3_send
);

CREATE OR REPLACE FUNCTION vector3_minus ( v0 vector3 )
RETURNS vector3 AS
'MODULE_PATHNAME', 'vector3_minus'
LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR -
(
    rightarg = vector3,
    procedure = vector3_minus
);

CREATE OR REPLACE FUNCTION vector3_add ( v0 vector3, v1 vector3 )
RETURNS vector3 AS
'MODULE_PATHNAME', 'vector3_add'
LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR +
(
    leftarg = vector3,
    rightarg = vector3,
    procedure = vector3_add,
    commutator = +
);

CREATE OR REPLACE FUNCTION vector3_sub ( v0 vector3, v1 vector3 )
RETURNS vector3 AS
'MODULE_PATHNAME', 'vector3_sub'
LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR -
(
    leftarg = vector3,
    rightarg = vector3,
    procedure = vector3_sub
);

CREATE OR REPLACE FUNCTION vector3_mul_left ( v0 vector3, k double precision )
RETURNS vector3 AS
'MODULE_PATHNAME', 'vector3_mul_left'
LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR *
(
    leftarg = vector3,
    rightarg = double precision,
    procedure = vector3_mul_left,
    commutator = *
);

CREATE OR REPLACE FUNCTION vector3_mul_right ( k double precision, v0 vector3 )
RETURNS vector3 AS
'MODULE_PATHNAME', 'vector3_mul_right'
LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR *
(
    leftarg = double precision,
    rightarg = vector3,
    procedure = vector3_mul_right,
    commutator = *
);

CREATE OR REPLACE FUNCTION vector3_div_left ( v0 vector3, k double precision )
RETURNS vector3 AS
'MODULE_PATHNAME', 'vector3_div_left'
LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR /
(
    leftarg = vector3,
    rightarg = double precision,
    procedure = vector3_div_left
);

CREATE OR REPLACE FUNCTION vector3_div_right ( k double precision, v0 vector3 )
RETURNS vector3 AS
'MODULE_PATHNAME', 'vector3_div_right'
LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR /
(
    leftarg = double precision,
    rightarg = vector3,
    procedure = vector3_div_right
);

CREATE OR REPLACE FUNCTION vector3_equal ( v0 vector3, v1 vector3 )
RETURNS boolean AS
'MODULE_PATHNAME', 'vector3_equal'
LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR =
(
    leftarg = vector3,
    rightarg = vector3,
    procedure = vector3_equal
);

CREATE OR REPLACE FUNCTION vector3_not_equal ( v0 vector3, v1 vector3 )
RETURNS boolean AS
'MODULE_PATHNAME', 'vector3_not_equal'
LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR !=
(
    leftarg = vector3,
    rightarg = vector3,
    procedure = vector3_not_equal
);

CREATE OR REPLACE FUNCTION vector3_dot ( v0 vector3, v1 vector3 )
RETURNS double precision AS
'MODULE_PATHNAME', 'vector3_dot'
LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR *
(
    leftarg = vector3,
    rightarg = vector3,
    procedure = vector3_dot,
    commutator = *
);

CREATE OR REPLACE FUNCTION vector3_cross ( v0 vector3, v1 vector3 )
RETURNS vector3 AS
'MODULE_PATHNAME', 'vector3_cross'
LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR **
(
    leftarg = vector3,
    rightarg = vector3,
    procedure = vector3_cross,
    commutator = **
);

CREATE OR REPLACE FUNCTION length ( v0 vector3 )
RETURNS double precision AS
'MODULE_PATHNAME', 'vector3_length'
LANGUAGE C IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION normalize ( v0 vector3 )
RETURNS vector3 AS
'MODULE_PATHNAME', 'vector3_normalize'
LANGUAGE C IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION distance ( v0 vector3, v1 vector3 )
RETURNS double precision AS
'MODULE_PATHNAME', 'vector3_distance'
LANGUAGE C IMMUTABLE STRICT;

CREATE TYPE vector3c AS
(
	x double precision,
	y double precision,
	z double precision
);

CREATE OR REPLACE FUNCTION vector3_cast_vector3c ( v0 vector3 )
RETURNS vector3c AS
$BODY$
DECLARE
	s text[];
	v vector3c;
BEGIN
	s := string_to_array ( trim ( BOTH '()' FROM v0::text ), ',' );
	v.x := s[1];
	v.y := s[2];
	v.z := s[3];
	RETURN v;
END
$BODY$
LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION vector3c_cast_vector3 ( v0 vector3c )
RETURNS vector3 AS
$BODY$
DECLARE
	v vector3;
BEGIN
	v := v0::text;
	RETURN v;
END
$BODY$
LANGUAGE plpgsql IMMUTABLE;

CREATE CAST ( vector3 AS vector3c )
WITH FUNCTION  vector3_cast_vector3c ( v0 vector3 )
AS IMPLICIT;

CREATE CAST ( vector3c AS vector3 )
WITH FUNCTION  vector3c_cast_vector3 ( v0 vector3c )
AS IMPLICIT;
