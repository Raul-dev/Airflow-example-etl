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
