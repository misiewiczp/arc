// THIS IS AN AUTOMATICALLY GENERATED FILE.  DO NOT MODIFY
// BY HAND!!
//
// Generated by lcm-gen

#include <string.h>
#include "arc_res_plan_mpc_t.h"

static int __arc_res_plan_mpc_t_hash_computed;
static uint64_t __arc_res_plan_mpc_t_hash;

uint64_t __arc_res_plan_mpc_t_hash_recursive(const __lcm_hash_ptr *p)
{
    const __lcm_hash_ptr *fp;
    for (fp = p; fp != NULL; fp = fp->parent)
        if (fp->v == __arc_res_plan_mpc_t_get_hash)
            return 0;

    __lcm_hash_ptr cp;
    cp.parent =  p;
    cp.v = __arc_res_plan_mpc_t_get_hash;
    (void) cp;

    uint64_t hash = (uint64_t)0x19739f11f8ec7910LL
         + __int64_t_hash_recursive(&cp)
         + __int64_t_hash_recursive(&cp)
         + __double_hash_recursive(&cp)
         + __double_hash_recursive(&cp)
         + __int32_t_hash_recursive(&cp)
         + __double_hash_recursive(&cp)
         + __double_hash_recursive(&cp)
        ;

    return (hash<<1) + ((hash>>63)&1);
}

int64_t __arc_res_plan_mpc_t_get_hash(void)
{
    if (!__arc_res_plan_mpc_t_hash_computed) {
        __arc_res_plan_mpc_t_hash = (int64_t)__arc_res_plan_mpc_t_hash_recursive(NULL);
        __arc_res_plan_mpc_t_hash_computed = 1;
    }

    return __arc_res_plan_mpc_t_hash;
}

int __arc_res_plan_mpc_t_encode_array(void *buf, int offset, int maxlen, const arc_res_plan_mpc_t *p, int elements)
{
    int pos = 0, element;
    int thislen;

    for (element = 0; element < elements; element++) {

        thislen = __int64_t_encode_array(buf, offset + pos, maxlen - pos, &(p[element].timestamp), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __int64_t_encode_array(buf, offset + pos, maxlen - pos, &(p[element].req_timestamp), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __double_encode_array(buf, offset + pos, maxlen - pos, &(p[element].delta_dir), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __double_encode_array(buf, offset + pos, maxlen - pos, &(p[element].delta_acc), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __int32_t_encode_array(buf, offset + pos, maxlen - pos, &(p[element].npoints), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __double_encode_array(buf, offset + pos, maxlen - pos, p[element].points_x, p[element].npoints);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __double_encode_array(buf, offset + pos, maxlen - pos, p[element].points_y, p[element].npoints);
        if (thislen < 0) return thislen; else pos += thislen;

    }
    return pos;
}

int arc_res_plan_mpc_t_encode(void *buf, int offset, int maxlen, const arc_res_plan_mpc_t *p)
{
    int pos = 0, thislen;
    int64_t hash = __arc_res_plan_mpc_t_get_hash();

    thislen = __int64_t_encode_array(buf, offset + pos, maxlen - pos, &hash, 1);
    if (thislen < 0) return thislen; else pos += thislen;

    thislen = __arc_res_plan_mpc_t_encode_array(buf, offset + pos, maxlen - pos, p, 1);
    if (thislen < 0) return thislen; else pos += thislen;

    return pos;
}

int __arc_res_plan_mpc_t_encoded_array_size(const arc_res_plan_mpc_t *p, int elements)
{
    int size = 0, element;
    for (element = 0; element < elements; element++) {

        size += __int64_t_encoded_array_size(&(p[element].timestamp), 1);

        size += __int64_t_encoded_array_size(&(p[element].req_timestamp), 1);

        size += __double_encoded_array_size(&(p[element].delta_dir), 1);

        size += __double_encoded_array_size(&(p[element].delta_acc), 1);

        size += __int32_t_encoded_array_size(&(p[element].npoints), 1);

        size += __double_encoded_array_size(p[element].points_x, p[element].npoints);

        size += __double_encoded_array_size(p[element].points_y, p[element].npoints);

    }
    return size;
}

int arc_res_plan_mpc_t_encoded_size(const arc_res_plan_mpc_t *p)
{
    return 8 + __arc_res_plan_mpc_t_encoded_array_size(p, 1);
}

int __arc_res_plan_mpc_t_decode_array(const void *buf, int offset, int maxlen, arc_res_plan_mpc_t *p, int elements)
{
    int pos = 0, thislen, element;

    for (element = 0; element < elements; element++) {

        thislen = __int64_t_decode_array(buf, offset + pos, maxlen - pos, &(p[element].timestamp), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __int64_t_decode_array(buf, offset + pos, maxlen - pos, &(p[element].req_timestamp), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __double_decode_array(buf, offset + pos, maxlen - pos, &(p[element].delta_dir), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __double_decode_array(buf, offset + pos, maxlen - pos, &(p[element].delta_acc), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __int32_t_decode_array(buf, offset + pos, maxlen - pos, &(p[element].npoints), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        p[element].points_x = (double*) lcm_malloc(sizeof(double) * p[element].npoints);
        thislen = __double_decode_array(buf, offset + pos, maxlen - pos, p[element].points_x, p[element].npoints);
        if (thislen < 0) return thislen; else pos += thislen;

        p[element].points_y = (double*) lcm_malloc(sizeof(double) * p[element].npoints);
        thislen = __double_decode_array(buf, offset + pos, maxlen - pos, p[element].points_y, p[element].npoints);
        if (thislen < 0) return thislen; else pos += thislen;

    }
    return pos;
}

int __arc_res_plan_mpc_t_decode_array_cleanup(arc_res_plan_mpc_t *p, int elements)
{
    int element;
    for (element = 0; element < elements; element++) {

        __int64_t_decode_array_cleanup(&(p[element].timestamp), 1);

        __int64_t_decode_array_cleanup(&(p[element].req_timestamp), 1);

        __double_decode_array_cleanup(&(p[element].delta_dir), 1);

        __double_decode_array_cleanup(&(p[element].delta_acc), 1);

        __int32_t_decode_array_cleanup(&(p[element].npoints), 1);

        __double_decode_array_cleanup(p[element].points_x, p[element].npoints);
        if (p[element].points_x) free(p[element].points_x);

        __double_decode_array_cleanup(p[element].points_y, p[element].npoints);
        if (p[element].points_y) free(p[element].points_y);

    }
    return 0;
}

int arc_res_plan_mpc_t_decode(const void *buf, int offset, int maxlen, arc_res_plan_mpc_t *p)
{
    int pos = 0, thislen;
    int64_t hash = __arc_res_plan_mpc_t_get_hash();

    int64_t this_hash;
    thislen = __int64_t_decode_array(buf, offset + pos, maxlen - pos, &this_hash, 1);
    if (thislen < 0) return thislen; else pos += thislen;
    if (this_hash != hash) return -1;

    thislen = __arc_res_plan_mpc_t_decode_array(buf, offset + pos, maxlen - pos, p, 1);
    if (thislen < 0) return thislen; else pos += thislen;

    return pos;
}

int arc_res_plan_mpc_t_decode_cleanup(arc_res_plan_mpc_t *p)
{
    return __arc_res_plan_mpc_t_decode_array_cleanup(p, 1);
}

int __arc_res_plan_mpc_t_clone_array(const arc_res_plan_mpc_t *p, arc_res_plan_mpc_t *q, int elements)
{
    int element;
    for (element = 0; element < elements; element++) {

        __int64_t_clone_array(&(p[element].timestamp), &(q[element].timestamp), 1);

        __int64_t_clone_array(&(p[element].req_timestamp), &(q[element].req_timestamp), 1);

        __double_clone_array(&(p[element].delta_dir), &(q[element].delta_dir), 1);

        __double_clone_array(&(p[element].delta_acc), &(q[element].delta_acc), 1);

        __int32_t_clone_array(&(p[element].npoints), &(q[element].npoints), 1);

        q[element].points_x = (double*) lcm_malloc(sizeof(double) * q[element].npoints);
        __double_clone_array(p[element].points_x, q[element].points_x, p[element].npoints);

        q[element].points_y = (double*) lcm_malloc(sizeof(double) * q[element].npoints);
        __double_clone_array(p[element].points_y, q[element].points_y, p[element].npoints);

    }
    return 0;
}

arc_res_plan_mpc_t *arc_res_plan_mpc_t_copy(const arc_res_plan_mpc_t *p)
{
    arc_res_plan_mpc_t *q = (arc_res_plan_mpc_t*) malloc(sizeof(arc_res_plan_mpc_t));
    __arc_res_plan_mpc_t_clone_array(p, q, 1);
    return q;
}

void arc_res_plan_mpc_t_destroy(arc_res_plan_mpc_t *p)
{
    __arc_res_plan_mpc_t_decode_array_cleanup(p, 1);
    free(p);
}

int arc_res_plan_mpc_t_publish(lcm_t *lc, const char *channel, const arc_res_plan_mpc_t *p)
{
      int max_data_size = arc_res_plan_mpc_t_encoded_size (p);
      uint8_t *buf = (uint8_t*) malloc (max_data_size);
      if (!buf) return -1;
      int data_size = arc_res_plan_mpc_t_encode (buf, 0, max_data_size, p);
      if (data_size < 0) {
          free (buf);
          return data_size;
      }
      int status = lcm_publish (lc, channel, buf, data_size);
      free (buf);
      return status;
}

struct _arc_res_plan_mpc_t_subscription_t {
    arc_res_plan_mpc_t_handler_t user_handler;
    void *userdata;
    lcm_subscription_t *lc_h;
};
static
void arc_res_plan_mpc_t_handler_stub (const lcm_recv_buf_t *rbuf,
                            const char *channel, void *userdata)
{
    int status;
    arc_res_plan_mpc_t p;
    memset(&p, 0, sizeof(arc_res_plan_mpc_t));
    status = arc_res_plan_mpc_t_decode (rbuf->data, 0, rbuf->data_size, &p);
    if (status < 0) {
        fprintf (stderr, "error %d decoding arc_res_plan_mpc_t!!!\n", status);
        return;
    }

    arc_res_plan_mpc_t_subscription_t *h = (arc_res_plan_mpc_t_subscription_t*) userdata;
    h->user_handler (rbuf, channel, &p, h->userdata);

    arc_res_plan_mpc_t_decode_cleanup (&p);
}

arc_res_plan_mpc_t_subscription_t* arc_res_plan_mpc_t_subscribe (lcm_t *lcm,
                    const char *channel,
                    arc_res_plan_mpc_t_handler_t f, void *userdata)
{
    arc_res_plan_mpc_t_subscription_t *n = (arc_res_plan_mpc_t_subscription_t*)
                       malloc(sizeof(arc_res_plan_mpc_t_subscription_t));
    n->user_handler = f;
    n->userdata = userdata;
    n->lc_h = lcm_subscribe (lcm, channel,
                                 arc_res_plan_mpc_t_handler_stub, n);
    if (n->lc_h == NULL) {
        fprintf (stderr,"couldn't reg arc_res_plan_mpc_t LCM handler!\n");
        free (n);
        return NULL;
    }
    return n;
}

int arc_res_plan_mpc_t_subscription_set_queue_capacity (arc_res_plan_mpc_t_subscription_t* subs,
                              int num_messages)
{
    return lcm_subscription_set_queue_capacity (subs->lc_h, num_messages);
}

int arc_res_plan_mpc_t_unsubscribe(lcm_t *lcm, arc_res_plan_mpc_t_subscription_t* hid)
{
    int status = lcm_unsubscribe (lcm, hid->lc_h);
    if (0 != status) {
        fprintf(stderr,
           "couldn't unsubscribe arc_res_plan_mpc_t_handler %p!\n", hid);
        return -1;
    }
    free (hid);
    return 0;
}

