import time
import threading
import logging as log

log.getLogger(__name__)

import cv2

from config import config


class PIDController:
    def __init__(
        self, setpoint, output, kp, ki, kd, call, threshold=0, finalcall=None
    ):
        """Implements a PID controller.

        Parameters
        ----------
        setpoint: float
            The the value that the PID controller should try to reach.
        output: float
            The initial output value to try.
        kp: float
            The proportional coefficient.
        ki: float
            The integral coefficient.
        kd: float
            The derivative coefficient.
        call: function
            The function to call to obtain the measured value.
        threshold: float
            The acceptable error level for the measured value.
        finalcall: function
            A function to be called after the threshold is reached.
        """

        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.call = call
        self.finalcall = finalcall
        self.output = output

        self.integral = 0

    def update(self):
        """Run one pass of the PID controller and update values.
        """

        try:
            last_error = self.error
            last_time = self.time
        except AttributeError:
            self.error = self.setpoint - self.call(self.output)
            self.last_time = time.time()
        else:
            error = self.setpoint - self.call(self.output)
            current_time = time.time()
            dt = current_time - self.last_time
            self.last_time = current_time

            self.integral += error * dt
            derivative = (error - self.last_error) / dt
            self.error = error
            self.output = kp * self.error + ki * integral + kd * derivative
        return self.error < threshold

    def run(self):
        """Continuously run the PID controller until threshold is reached.
        """
        while update():
            time.sleep(self.timestep)
        if self.lastcall is not None:
            self.lastcall()


class IODevice:
    """A wrapper class for Input/Output devices.

    This class is inherited by IO device classes and ensures they have required
    methods and attributes defined.
    """

    def __init__(self, samplerate=0):
        self.samplerate = samplerate

    def setup(self):
        log.info("No setup function defined for %s." % self.__class__.__name__)

    def cleanup(self):
        log.info(
            "No cleanup function defined for %s." % self.__class__.__name__
        )

    def read(self, voltage_label, *args, **kwargs):
        log.info("No read function defined for %s." % self.__class__.__name__)

    def output(self, *args, **kwargs):
        log.info(
            "No output function defined for %s." % self.__class__.__name__
        )


class WebcamVelocity:
    """A velocity mode implementation for a Kibble balance using a webcam.

    Uses a provided input/output device to control the movement of the
    Kibble balance and read the coil voltage and a webcam to determine
    the velocity of the Kibble balance during movement.

    Parameters
    ----------
    io_device: IODevice
        A subclass of the umdkb.IODevice class. Must have a .read_voltage() method
        able to read the coil_voltage and an oscillate() method to actuate the
        kibble balance.
    camera_index: int, optional
        The index of the camera device to use with opencv.

    Attributes
    ----------
    frames: list(numpy.ndarray)
        A list of numpy arrays containing the pixel values recorded for each
        frame. An single item in the list corresponds to a single frame.
    """

    def __init__(self, io_device, camera_index=0):
        self._camera_index = camera_index
        self._capture_device = cv2.VideoCapture(camera_index)
        self._io_device = io_device
        self._recorder = VideoRecorder(self._capture_device)
        self.frames = None

    def calcfps(self, frames_to_read=120, force_calc=False):
        """Determines the frame rate of the capture device.

        If possible, the frame rate is determined by the camera properties
        using opencv. If not, an estimation is made based on elapsed time.

        Parameters
        ----------
        frames_to_read: int, optional
            The number of frames to read for the estimation.
        force_estimate: bool, optional
            If true, the frame rate will be estimated even if it can be
            determined by opencv.

        Returns
        -------
        int:
            The frame rate of the device.
        """
        fps = self._capture_device.get(cv2.CAP_PROP_FPS)
        if fps == 0 or force_calc:
            log.warn("Unable to determine frame rate of device. Estimating...")
            frames_to_check = 500
            start = time.time()
            for i in range(frames_to_check - 1):
                ret, frame = self._capture_device.read()
            stop = time.time()
            fps = frames_to_check / (stop - start)
            log.info("Estimated FPS is %f." % fps)
        else:
            log.info("The camera frame rate is %f." % fps)
        return round(fps)

    def start_recording(self):
        """Starts recording video frames."""
        self._recorder.start()

    def stop_recording(self):
        """Stops recording video frames and sets the self.frames attribute."""
        self.frames = self._recorder.stop()
        self._capture_device.release()


class VideoRecorder(threading.Thread):
    """Records video from a capture device.

    Uses a separate thread to start saving frames from a provided
    capture_device.  The saved frames can later be returned when the recording
    is stopped.

    Parameters
    ----------
    capture_device: cv2.VideoCapture
        The device to record from.
    """

    def __init__(self, capture_device):
        super().__init__()
        self._recording = True
        self._capture_device = capture_device
        self._frames = []

    def run(self):
        """Start recording frames from the capture device."""
        while self._recording:
            ret, frame = self._capture_device.read()
            self._frames.append(frame)

    def stop(self):
        """Stop recording and return the video frames.

        Returns
        -------
        list(numpy.ndarray)
            The recorded frames.
        """
        self._recording = False

        # Ensure that recording is finished before returning frames.
        time.sleep(0.5)
        return self._frames
