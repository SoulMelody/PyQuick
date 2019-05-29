import cffi
from ctypes.util import find_library


ffi = cffi.FFI()
ffi.cdef('''
typedef void DosQVariant;
typedef void DosQModelIndex;
typedef void DosQAbstractItemModel;
typedef void DosQAbstractListModel;
typedef void DosQAbstractTableModel;
typedef void DosQQmlApplicationEngine;
typedef void DosQQuickView;
typedef void DosQQmlContext;
typedef void DosQHashIntQByteArray;
typedef void DosQUrl;
typedef void DosQMetaObject;
typedef void DosQObject;
typedef void DosQQuickImageProvider;
typedef void DosPixmap;
typedef void ( *RequestPixmapCallback)(const char *id, int *width, int *height, int requestedWidth, int requestedHeight, DosPixmap* result);
typedef void ( *DObjectCallback)(void *self, DosQVariant *slotName, int argc, DosQVariant **argv);
typedef void ( *RowCountCallback)(void *self, const DosQModelIndex *parent, int *result);
typedef void ( *ColumnCountCallback)(void *self, const DosQModelIndex *parent, int *result);
typedef void ( *DataCallback)(void *self, const DosQModelIndex *index, int role, DosQVariant *result);
typedef void ( *SetDataCallback)(void *self, const DosQModelIndex *index, const DosQVariant *value, int role, _Bool *result);
typedef void ( *RoleNamesCallback)(void *self, DosQHashIntQByteArray *result);
typedef void ( *FlagsCallback)(void *self, const DosQModelIndex *index, int *result);
typedef void ( *HeaderDataCallback)(void *self, int section, int orientation, int role, DosQVariant *result);
typedef void ( *IndexCallback)(void *self, int row, int column, const DosQModelIndex *parent, DosQModelIndex *result);
typedef void ( *ParentCallback)(void *self, const DosQModelIndex *child, DosQModelIndex *result);
typedef void ( *HasChildrenCallback)(void *self, const DosQModelIndex *parent, _Bool *result);
typedef void ( *CanFetchMoreCallback)(void *self, const DosQModelIndex *parent, _Bool *result);
typedef void ( *FetchMoreCallback)(void *self, const DosQModelIndex *parent);
typedef void ( *CreateDObject)(int id, void *wrapper, void **bindedQObject, void **dosQObject);
typedef void ( *DeleteDObject)(int id, void *bindedQObject);
struct DosQVariantArray {
    int size;
    DosQVariant **data;
};
typedef struct DosQVariantArray DosQVariantArray;
struct QmlRegisterType {
    int major;
    int minor;
    const char *uri;
    const char *qml;
    DosQMetaObject *staticMetaObject;
    CreateDObject createDObject;
    DeleteDObject deleteDObject;
};
typedef struct QmlRegisterType QmlRegisterType;
struct ParameterDefinition {
    const char *name;
    int metaType;
};
typedef struct ParameterDefinition ParameterDefinition;
struct SignalDefinition {
    const char *name;
    int parametersCount;
    ParameterDefinition *parameters;
};
typedef struct SignalDefinition SignalDefinition;
struct SignalDefinitions {
    int count;
    SignalDefinition *definitions;
};
typedef struct SignalDefinitions SignalDefinitions;
struct SlotDefinition {
    const char *name;
    int returnMetaType;
    int parametersCount;
    ParameterDefinition *parameters;
};
typedef struct SlotDefinition SlotDefinition;
struct SlotDefinitions {
    int count;
    SlotDefinition *definitions;
};
typedef struct SlotDefinitions SlotDefinitions;
struct PropertyDefinition {
    const char *name;
    int propertyMetaType;
    const char *readSlot;
    const char *writeSlot;
    const char *notifySignal;
};
typedef struct PropertyDefinition PropertyDefinition;
struct PropertyDefinitions {
    int count;
    PropertyDefinition *definitions;
};
typedef struct PropertyDefinitions PropertyDefinitions;
struct DosQAbstractItemModelCallbacks {
    RowCountCallback rowCount;
    ColumnCountCallback columnCount;
    DataCallback data;
    SetDataCallback setData;
    RoleNamesCallback roleNames;
    FlagsCallback flags;
    HeaderDataCallback headerData;
    IndexCallback index;
    ParentCallback parent;
    HasChildrenCallback hasChildren;
    CanFetchMoreCallback canFetchMore;
    FetchMoreCallback fetchMore;
};
typedef struct DosQAbstractItemModelCallbacks DosQAbstractItemModelCallbacks;
char * dos_qcoreapplication_application_dir_path();
void dos_qguiapplication_create();
void dos_qguiapplication_exec();
void dos_qguiapplication_quit();
void dos_qguiapplication_delete();
void dos_qapplication_create();
void dos_qapplication_exec();
void dos_qapplication_quit();
void dos_qapplication_delete();
DosQQmlApplicationEngine * dos_qqmlapplicationengine_create();
void dos_qqmlapplicationengine_load(DosQQmlApplicationEngine *vptr, const char *filename);
void dos_qqmlapplicationengine_load_url(DosQQmlApplicationEngine *vptr, DosQUrl *url);
void dos_qqmlapplicationengine_load_data(DosQQmlApplicationEngine *vptr, const char *data);
void dos_qqmlapplicationengine_add_import_path(DosQQmlApplicationEngine *vptr, const char *path);
DosQQmlContext * dos_qqmlapplicationengine_context(DosQQmlApplicationEngine *vptr);
void dos_qqmlapplicationengine_addImageProvider(DosQQmlApplicationEngine *vptr, const char* name, DosQQuickImageProvider *vptr_i);
void dos_qqmlapplicationengine_delete(DosQQmlApplicationEngine *vptr);
DosQQuickImageProvider * dos_qquickimageprovider_create(RequestPixmapCallback callback);
void dos_qquickimageprovider_delete(DosQQuickImageProvider *vptr);
DosPixmap * dos_qpixmap_create();
DosPixmap * dos_qpixmap_create_qpixmap(const DosPixmap* other);
DosPixmap * dos_qpixmap_create_width_and_height(int width, int height);
void dos_qpixmap_delete(DosPixmap *vptr);
void dos_qpixmap_load(DosPixmap *vptr, const char* filepath, const char* format);
void dos_qpixmap_loadFromData(DosPixmap *vptr, const unsigned char* data, unsigned int len);
void dos_qpixmap_fill(DosPixmap *vptr, unsigned char r, unsigned char g, unsigned char b, unsigned char a);
void dos_qpixmap_assign(DosPixmap *vptr, const DosPixmap* other);
_Bool dos_qpixmap_isNull(DosPixmap *vptr);
void dos_qquickstyle_set_style(const char *style);
void dos_qquickstyle_set_fallback_style(const char *style);
DosQQuickView * dos_qquickview_create();
void dos_qquickview_show(DosQQuickView *vptr);
char * dos_qquickview_source(const DosQQuickView *vptr);
void dos_qquickview_set_source_url(DosQQuickView *vptr, DosQUrl *url);
void dos_qquickview_set_source(DosQQuickView *vptr, const char *filename);
void dos_qquickview_set_resize_mode(DosQQuickView *vptr, int resizeMode);
void dos_qquickview_delete(DosQQuickView *vptr);
DosQQmlContext * dos_qquickview_rootContext(DosQQuickView *vptr);
char * dos_qqmlcontext_baseUrl(const DosQQmlContext *vptr);
void dos_qqmlcontext_setcontextproperty(DosQQmlContext *vptr, const char *name, DosQVariant *value);
void dos_chararray_delete(char *ptr);
void dos_qvariantarray_delete(DosQVariantArray *ptr);
DosQVariant * dos_qvariant_create();
DosQVariant * dos_qvariant_create_int(int value);
DosQVariant * dos_qvariant_create_bool(_Bool value);
DosQVariant * dos_qvariant_create_string(const char *value);
DosQVariant * dos_qvariant_create_qobject(DosQObject *value);
DosQVariant * dos_qvariant_create_qvariant(const DosQVariant *value);
DosQVariant * dos_qvariant_create_float(float value);
DosQVariant * dos_qvariant_create_double(double value);
DosQVariant * dos_qvariant_create_array(int size, DosQVariant **array);
void dos_qvariant_setInt(DosQVariant *vptr, int value);
void dos_qvariant_setBool(DosQVariant *vptr, _Bool value);
void dos_qvariant_setFloat(DosQVariant *vptr, float value);
void dos_qvariant_setDouble(DosQVariant *vptr, double value);
void dos_qvariant_setString(DosQVariant *vptr, const char *value);
void dos_qvariant_setQObject(DosQVariant *vptr, DosQObject *value);
void dos_qvariant_setArray(DosQVariant *vptr, int size, DosQVariant **array);
_Bool dos_qvariant_isnull(const DosQVariant *vptr);
void dos_qvariant_delete(DosQVariant *vptr);
void dos_qvariant_assign(DosQVariant *vptr, const DosQVariant *other);
int dos_qvariant_toInt(const DosQVariant *vptr);
_Bool dos_qvariant_toBool(const DosQVariant *vptr);
char * dos_qvariant_toString(const DosQVariant *vptr);
float dos_qvariant_toFloat (const DosQVariant *vptr);
double dos_qvariant_toDouble(const DosQVariant *vptr);
DosQVariantArray * dos_qvariant_toArray(const DosQVariant *vptr);
DosQObject * dos_qvariant_toQObject(const DosQVariant *vptr);
DosQMetaObject * dos_qmetaobject_create(DosQMetaObject *superClassMetaObject,
                                                const char *className,
                                                const SignalDefinitions *signalDefinitions,
                                                const SlotDefinitions *slotDefinitions,
                                                const PropertyDefinitions *propertyDefinitions);
void dos_qmetaobject_delete(DosQMetaObject *vptr);
DosQMetaObject * dos_qabstractlistmodel_qmetaobject();
DosQAbstractListModel * dos_qabstractlistmodel_create(void *callbackObject,
                                                                DosQMetaObject *metaObject,
                                                                DObjectCallback dObjectCallback,
                                                                DosQAbstractItemModelCallbacks *callbacks);
DosQModelIndex * dos_qabstractlistmodel_index(DosQAbstractListModel *vptr,
                                                        int row, int column, DosQModelIndex *parent);
DosQModelIndex * dos_qabstractlistmodel_parent(DosQAbstractListModel *vptr,
                                                        DosQModelIndex *child);
int dos_qabstractlistmodel_columnCount(DosQAbstractListModel *vptr,
                                                DosQModelIndex *parent);
DosQMetaObject * dos_qabstracttablemodel_qmetaobject();
DosQAbstractTableModel * dos_qabstracttablemodel_create(void *callbackObject,
                                                                DosQMetaObject *metaObject,
                                                                DObjectCallback dObjectCallback,
                                                                DosQAbstractItemModelCallbacks *callbacks);
DosQModelIndex * dos_qabstracttablemodel_index(DosQAbstractTableModel *vptr,
                                                        int row, int column, DosQModelIndex *parent);
DosQModelIndex * dos_qabstracttablemodel_parent(DosQAbstractTableModel *vptr,
                                                        DosQModelIndex *child);
DosQMetaObject * dos_qabstractitemmodel_qmetaobject();
DosQAbstractItemModel * dos_qabstractitemmodel_create(void *callbackObject,
                                                                DosQMetaObject *metaObject,
                                                                DObjectCallback dObjectCallback,
                                                                DosQAbstractItemModelCallbacks *callbacks);
int dos_qabstractitemmodel_flags(DosQAbstractItemModel *vptr, DosQModelIndex *index);
_Bool dos_qabstractitemmodel_hasChildren(DosQAbstractItemModel *vptr, DosQModelIndex *parentIndex);
_Bool dos_qabstractitemmodel_hasIndex(DosQAbstractItemModel *vptr, int row, int column, DosQModelIndex *dosParentIndex);
_Bool dos_qabstractitemmodel_canFetchMore(DosQAbstractItemModel *vptr, DosQModelIndex *parentIndex);
void dos_qabstractitemmodel_fetchMore(DosQAbstractItemModel *vptr, DosQModelIndex *parentIndex);
void dos_qabstractitemmodel_beginInsertRows(DosQAbstractItemModel *vptr, DosQModelIndex *parent, int first, int last);
void dos_qabstractitemmodel_endInsertRows(DosQAbstractItemModel *vptr);
void dos_qabstractitemmodel_beginRemoveRows(DosQAbstractItemModel *vptr, DosQModelIndex *parent, int first, int last);
void dos_qabstractitemmodel_endRemoveRows(DosQAbstractItemModel *vptr);
void dos_qabstractitemmodel_beginInsertColumns(DosQAbstractItemModel *vptr, DosQModelIndex *parent, int first, int last);
void dos_qabstractitemmodel_endInsertColumns(DosQAbstractItemModel *vptr);
void dos_qabstractitemmodel_beginRemoveColumns(DosQAbstractItemModel *vptr, DosQModelIndex *parent, int first, int last);
void dos_qabstractitemmodel_endRemoveColumns(DosQAbstractItemModel *vptr);
void dos_qabstractitemmodel_beginResetModel(DosQAbstractItemModel *vptr);
void dos_qabstractitemmodel_endResetModel(DosQAbstractItemModel *vptr);
void dos_qabstractitemmodel_dataChanged(DosQAbstractItemModel *vptr,
                                                    const DosQModelIndex *topLeft,
                                                    const DosQModelIndex *bottomRight,
                                                    int *rolesPtr, int rolesLength);
DosQModelIndex * dos_qabstractitemmodel_createIndex(DosQAbstractItemModel *vptr,
                                                            int row, int column, void *data);
_Bool dos_qabstractitemmodel_setData(DosQAbstractItemModel *vptr,
                                                DosQModelIndex *index, DosQVariant *value, int role);
DosQHashIntQByteArray * dos_qabstractitemmodel_roleNames(DosQAbstractItemModel *vptr);
DosQVariant * dos_qabstractitemmodel_headerData(DosQAbstractItemModel *vptr,
                                                        int section, int orientation, int role);
DosQMetaObject * dos_qobject_qmetaobject();
DosQObject * dos_qobject_create(void *dObjectPointer,
                                        DosQMetaObject *metaObject,
                                        DObjectCallback dObjectCallback);
void dos_qobject_signal_emit(DosQObject *vptr,
                                        const char *name,
                                        int parametersCount,
                                        void **parameters);
_Bool dos_qobject_signal_connect(DosQObject *senderVPtr,
                                            const char *signal,
                                            DosQObject *receiverVPtr,
                                            const char *method,
                                            int type);
_Bool dos_qobject_signal_disconnect(DosQObject *senderVPtr,
                                            const char *signal,
                                            DosQObject *receiverVPtr,
                                            const char *method);
char * dos_qobject_objectName(const DosQObject *vptr);
void dos_qobject_setObjectName(DosQObject *vptr, const char *name);
void dos_qobject_delete(DosQObject *vptr);
void dos_qobject_deleteLater(DosQObject *vptr);
DosQVariant * dos_qobject_property(DosQObject *vptr,
                                        const char *propertyName);
_Bool dos_qobject_setProperty(DosQObject *vptr,
                                            const char *propertyName,
                                            DosQVariant *value);
DosQModelIndex * dos_qmodelindex_create();
DosQModelIndex * dos_qmodelindex_create_qmodelindex(DosQModelIndex *index);
void dos_qmodelindex_delete (DosQModelIndex *vptr);
int dos_qmodelindex_row (const DosQModelIndex *vptr);
int dos_qmodelindex_column (const DosQModelIndex *vptr);
_Bool dos_qmodelindex_isValid(const DosQModelIndex *vptr);
DosQVariant * dos_qmodelindex_data (const DosQModelIndex *vptr, int role);
DosQModelIndex * dos_qmodelindex_parent (const DosQModelIndex *vptr);
DosQModelIndex * dos_qmodelindex_child (const DosQModelIndex *vptr, int row, int column);
DosQModelIndex * dos_qmodelindex_sibling(const DosQModelIndex *vptr, int row, int column);
void dos_qmodelindex_assign(DosQModelIndex *l, const DosQModelIndex *r);
void* dos_qmodelindex_internalPointer(DosQModelIndex *vptr);
DosQHashIntQByteArray * dos_qhash_int_qbytearray_create();
void dos_qhash_int_qbytearray_delete(DosQHashIntQByteArray *vptr);
void dos_qhash_int_qbytearray_insert(DosQHashIntQByteArray *vptr, int key, const char *value);
char * dos_qhash_int_qbytearray_value(const DosQHashIntQByteArray *vptr, int key);
void dos_qresource_register(const char *filename);
DosQUrl * dos_qurl_create(const char *url, int parsingMode);
void dos_qurl_delete(DosQUrl *vptr);
char * dos_qurl_to_string(const DosQUrl *vptr);
_Bool dos_qurl_isValid(const DosQUrl *vptr);
int dos_qdeclarative_qmlregistertype(const QmlRegisterType *qmlRegisterType);
int dos_qdeclarative_qmlregistersingletontype(const QmlRegisterType *qmlRegisterType);
''')
lib = ffi.dlopen(find_library('DOtherSide'))
