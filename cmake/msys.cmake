ADD_COMPILE_OPTIONS(-Wall)
SET (FLEX flex)
SET (BISON bison)

SET (BOOST_INCLUDE "${CONDA_PREFIX}/Library/include")
ADD_DEFINITIONS(-DBOOST_NO_CXX14_CONSTEXPR)
#ADD_DEFINITIONS(-DSTATIC_BUILD -D_USE_MATH_DEFINES)

#SET (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /fp:strict /EHsc ${WARNINGS_IGNORE}")
#SET (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /fp:strict ${WARNINGS_IGNORE}")

#SET (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /SAFESEH:NO")
#SET (CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} /SAFESEH:NO /NODEFAULTLIB:python3")
#SET (CMAKE_MODULE_LINKER_FLAGS "${CMAKE_MODULE_LINKER_FLAGS} /SAFESEH:NO")

# windows build

SET (SUPERLULOCATE   ${CMAKE_SOURCE_DIR}/external/superlu)
SET (SUPERLU_ARCHIVE ${SUPERLULOCATE}/msys/SRC/libsuperlu.a)
SET (SUPERLU_INCLUDE ${SUPERLULOCATE}/SRC)

SET (BLAS_ARCHIVE          ${CONDA_PREFIX}/Library/lib/mkl_rt.lib)
SET (EXTENDED_BLAS_ARCHIVE ${CMAKE_SOURCE_DIR}/external/getrf/msys/libgetrf.a)
SET (MKL_PARDISO_INCLUDE ${CONDA_PREFIX}/Library/include)

SET (SQLITE3_INCLUDE  ${CONDA_PREFIX}/Library/include)
SET (SQLITE3_ARCHIVE  ${CONDA_PREFIX}/Library/lib/sqlite3.lib)

SET (ZLIB_INCLUDE ${CONDA_PREFIX}/Library/include)
SET (ZLIB_ARCHIVE ${CONDA_PREFIX}/Library/lib/zlib.lib)

SET (SYMDIFF_INCLUDE ${CMAKE_SOURCE_DIR}/external/symdiff/include)
SET (SYMDIFF_ARCHIVE ${CMAKE_SOURCE_DIR}/external/symdiff/msys_x86_64_release/src/engine/libsymdiff_static.a)

SET (QUADMATH_ARCHIVE "-lquadmath")

